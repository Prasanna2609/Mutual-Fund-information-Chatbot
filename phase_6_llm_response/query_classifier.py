"""
query_classifier.py
Detects whether a user query is factual or advisory.
"""

import re

def is_advisory_query(query: str) -> bool:
    """
    Returns True if the query appears to be asking for advice, comparisons, or recommendations.
    """
    # Keywords that suggest advisory intent
    advisory_keywords = [
        r"\bbest\b", r"\bbetter\b", r"\brecommend", r"\bsuggest", r"should i", 
        r"highest return", r"\btop\s+(?:fund|mutual fund|performer)", r"\bcompare\b", r"\bpick\b", r"\badvice\b"
    ]
    
    query_lower = query.lower()
    for pattern in advisory_keywords:
        if re.search(pattern, query_lower):
            return True
            
    return False

def is_overview_query(query: str) -> bool:
    """
    Returns True if the query appears to be asking for a general dataset overview or list of all known funds.
    """
    overview_keywords = [
        r"\ball\s+funds\b", r"\bwhat\s+funds\b", r"\blist\b.*\bfunds\b", 
        r"\bdataset\s+overview\b", r"\bshow\s+me\s+all\b", r"\ball\s+the\s+data\b",
        r"\bfunds\s+by\s+category\b", r"\bwhat\s+do\s+you\s+know\b",
        r"^list\s+funds$", r"^show\s+all$"
    ]
    query_lower = query.strip().lower()
    for pattern in overview_keywords:
        if re.search(pattern, query_lower):
            return True
            
    return False

def is_amc_only_query(query: str) -> str:
    """
    Returns the AMC name if the query is ONLY a short AMC name (e.g., 'SBI', 'HDFC').
    Otherwise returns None.
    """
    amc_names = [
        "sbi", "hdfc", "icici", "nippon", "kotak", 
        "axis", "uti", "mirae", "quant", "tata", "groww", "hsbc"
    ]
    query_clean = query.strip().lower()
    if query_clean in amc_names:
        return query_clean
    return None

def is_relevant_query(query: str) -> bool:
    """
    Returns True if the query relates to mutual funds, schemes, NAV, SIP, expense ratio, 
    returns, AMC names, or dataset overview queries.
    """
    query_clean = query.strip().lower()
    
    # Simple garbage check: too short or random looking
    if len(query_clean) < 2:
        return False
        
    if is_overview_query(query_clean) or is_amc_only_query(query_clean):
        return True
        
    relevant_keywords = [
        r"\bfunds?\b", r"\bmutual\s+funds?\b", r"\bschemes?\b",
        r"\bnav\b", r"\bsip\b", r"\bexpense\s+ratio\b", r"\breturns?\b",
        r"\bamc\b", r"\bcap\b", r"\bgrowth\b", r"\bdividend\b", r"\byield\b",
        r"\binvest\b", r"\bequity\b", r"\bdebt\b", r"\bliquid\b", r"\bindex\b", r"\bportfolio\b",
        r"\bsbi\b", r"\bhdfc\b", r"\bicici\b", r"\bnippon\b", r"\bkotak\b", 
        r"\baxis\b", r"\buti\b", r"\bmirae\b", r"\bquant\b", r"\btata\b", r"\bgroww\b", r"\bhsbc\b"
    ]
    
    # Check for relevant keywords
    for pattern in relevant_keywords:
        if re.search(pattern, query_clean):
            return True
            
    return False


