"""
document_cleaner.py
Cleans redundant whitespace, line breaks, and non-ascii characters.
Ensures that key mutual fund attributes remain preserved.
"""
import re

def clean_text(text: str) -> str:
    """
    Applies regex to clean up redundant spaces or unstructured text artifacts
    that might confuse the embedding model or LLM.
    Important attributes like NAV, expense ratio, exit load, minimum SIP,
    benchmark index, risk level, fund manager, and AUM are preserved.
    """
    if not text:
        return ""
        
    # Replace multiple spaces with a single space
    cleaned = re.sub(r'[ \t]+', ' ', text)
    
    # --- Remove platform navigation/UI junk ---
    # We use more flexible regex (\s+) to handle varying whitespace
    junk_patterns = [
        r"Stocks\s+Invest\s+in\s+Stocks",
        r"Intraday\s+Monitor\s+top\s+intraday\s+performers",
        r"F&O\s+Trade\s+in\s+Futures\s+&\s+Options",
        r"API\s+trading",
        r"Stock\s+Screener",
        r"Terminal\s+Track\s+charts",
        r"Commodities\s+Trade\s+in\s+Crude\s+Oil",
        r"Option\s+chain\s+Analyse\s+chains",
        r"Pledge\s+Get\s+extra\s+balance",
        r"Brokerage\s+calculator",
        r"SWP\s+calculator",
        r"Margin\s+calculator",
        r"SIP\s+calculator",
        r"Mutual\s+Funds\s+Invest\s+in\s+Mutual\s+Funds",
        r"Indices\s+Track\s+markets\s+across\s+the\s+globe",
        r"Mutual\s+Fund\s+Houses\s+Know\s+about\s+AMCs",
        r"NFO’s\s+Track\s+all\s+active\s+NFOs",
        r"Track\s+Funds\s+Import\s+funds\s+and\s+track\s+all\s+investments",
        r"Compare\s+Funds\s+More",
        r"Demat\s+Account\s+Begin\s+your\s+stock\s+market\s+journey",
        r"Share\s+Market\s+Today\s+Live\s+news\s+updates",
        r"Estimate\s+charges\s+for\s+your\s+trade/investment",
        r"Estimate\s+balance\s+needed\s+to\s+buy/sell\s+a\s+stock",
        r"Returns\s+on\s+your\s+systematic\s+withdrawal\s+plan",
        r"Estimate\s+returns\s+on\s+a\s+SIP",
        r"Pricing\s+Brokerage\s+and\s+charges\s+on\s+Groww",
        r"Blog\s+\+\d+\.?\d*\s*%\s*\d+[YM]", # Catches things like "Blog +14.25 % 3Y"
        r"Start\s+SIP\s+Build\s+long-term\s+wealth\s+through\s+disciplined\s+monthly\s+investing",
        r"Mutual\s+funds\s+by\s+Groww\s+designed\s+for\s+your\s+investment\s+goals",
        r"Mutual\s+Funds\s+screener\s+Filter\s+funds\s+based\s+on\s+risk",
        r"Demat\s+Account\s+Begin\s+your\s+stock\s+market\s+journey",
        r"IPO\s+Track\s+upcoming\s+and\s+ongoing\s+IPOs",
        r"MTFs\s+Buy\s+now,\s+pay\s+later",
        r"Stock\s+Events\s+Dividends,\s+bonus,\s+buybacks",
        r"Live\s+news\s+updates\s+from\s+stock\s+market",
        r"Mutual\s+Funds\s+screener\s+Filter\s+funds\s+based\s+on\s+risk",
        r"Mutual\s+Funds\s+by\s+Groww\s+Mutual\s+funds\s+by\s+Groww",
        r"Pricing\s+Brokerage\s+and\s+charges\s+on\s+Groww\s+Blog",
        r"\bPricing\b\s*\bBlog\b"
    ]
    
    for pattern in junk_patterns:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)

    # Clean up residual artifacts and structural noise
    cleaned = re.sub(r'Pricing\s+Brokerage\s+and\s+charges\s+on\s+Groww\s+Blog', "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'annualised\s+[-+]?\d+\.?\d*\s*%\s*\d+[DWMY]', "", cleaned, flags=re.IGNORECASE)
    
    # Replace multiple spaces again after substitutions
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    
    # Replace multiple newlines with double newlines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    # Strip non-printable characters except basic whitespace
    cleaned = ''.join(c for c in cleaned if c.isprintable() or c in ['\n', '\r', '\t'])
    
    return cleaned.strip()
