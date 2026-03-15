"""
page_loader.py
Extracts readable text from a given HTML string using BeautifulSoup.
"""
from bs4 import BeautifulSoup

import json
from bs4 import BeautifulSoup
from typing import Dict, Tuple, Any

def extract_readable_text(html_content: str) -> str:
    """
    Parses HTML and extracts readable text by removing scripts, styling, 
    and navigation elements to minimize noise.
    """
    if not html_content:
        return ""
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove script, style, header, footer, and navigation tags
    # EXCEPT for the __NEXT_DATA__ script which we will handle separately if needed
    for tag in soup(["script", "style", "nav", "header", "footer", "noscript"]):
        if tag.get('id') != '__NEXT_DATA__':
            tag.extract()
        
    # Attempt to isolate main content
    main_content = soup.find('main') or soup.body
    
    if not main_content:
        main_content = soup

    # Extract text, compress multiple spaces and newlines
    text = main_content.get_text(separator=' ')
    cleaned_text = ' '.join(text.split())
    
    return cleaned_text

def extract_financial_data(html_content: str) -> Dict[str, Any]:
    """
    Extracts structured financial data from the __NEXT_DATA__ block.
    """
    if not html_content:
        return {}

    soup = BeautifulSoup(html_content, "html.parser")
    script = soup.find('script', id='__NEXT_DATA__')
    if not script:
        return {}

    def to_float(val):
        if val is None: return None
        try:
            # Handle potential string cleaning (e.g., removing %, ₹, or commas)
            clean_val = str(val).replace('%', '').replace('₹', '').replace(',', '').strip()
            return float(clean_val)
        except (ValueError, TypeError):
            return val

    try:
        data = json.loads(script.string)
        props = data.get('props', {})
        page_props = props.get('pageProps', {})
        # Data is mostly in mfServerSideData
        m = page_props.get('mfServerSideData', {})
        
        # Extract return stats safely
        r_stats = m.get("return_stats", [])
        primary_stats = r_stats[0] if r_stats else {}
        
        financials = {
            "nav": to_float(m.get("nav")),
            "nav_date": m.get("nav_date"),
            "riskometer": primary_stats.get("risk"),
            "min_sip": to_float(m.get("min_sip_investment")),
            "min_lumpsum": to_float(m.get("min_investment_amount")),
            "expense_ratio": to_float(m.get("expense_ratio")),
            "exit_load": m.get("exit_load"),
            "benchmark_index": m.get("benchmark_name"),
            "return_1y": to_float(primary_stats.get("return1y")),
            "return_3y": to_float(primary_stats.get("return3y")),
            "return_5y": to_float(primary_stats.get("return5y")),
            "aum": to_float(m.get("aum")),
            "fund_managers": [mgr.get("person_name") for mgr in m.get("fund_manager_details", [])] if m.get("fund_manager_details") else [],
            "top_holdings": [hld.get("company_name") for hld in m.get("holdings", [])[:10]] if m.get("holdings") else [],
            "lock_in_period": m.get("lock_in"),
            "factsheet_url": m.get("sid_url")
        }
        
        return financials
    except Exception as e:
        return {}

def extract_all(html_content: str) -> Tuple[str, Dict[str, Any]]:
    """
    Convenience function to get both text and structured data.
    """
    text = extract_readable_text(html_content)
    data = extract_financial_data(html_content)
    return text, data
