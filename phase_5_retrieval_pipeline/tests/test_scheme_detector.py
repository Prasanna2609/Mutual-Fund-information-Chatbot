import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from phase_5_retrieval_pipeline.scheme_detector import detect_scheme, ALIAS_MAPPING

def test_alias_detection():
    print("Testing alias detection...")
    known_schemes = [
        "SBI Bluechip Fund Direct Growth",
        "HDFC Top 100 Fund Direct Growth",
        "Nippon India Small Cap Fund Direct Growth"
    ]
    
    # 1. Test exact alias match
    query1 = "What is the NAV for SBI Large Cap?"
    scheme1 = detect_scheme(query1, known_schemes)
    assert scheme1 == "SBI Bluechip Fund Direct Growth", f"Expected SBI Bluechip Fund Direct Growth, got {scheme1}"
    
    # 2. Test another alias match
    query2 = "Tell me about hdfc large cap performance"
    scheme2 = detect_scheme(query2, known_schemes)
    assert scheme2 == "HDFC Top 100 Fund Direct Growth", f"Expected HDFC Top 100 Fund Direct Growth, got {scheme2}"
    
    # 3. Test conventional matching still works
    query3 = "What is the NAV of Nippon India Small Cap?"
    scheme3 = detect_scheme(query3, known_schemes)
    assert scheme3 == "Nippon India Small Cap Fund Direct Growth", f"Expected Nippon India Small Cap Fund Direct Growth, got {scheme3}"

    print("✓ Alias detection works correctly")
    print("✓ Conventional matching fallback works correctly")
    
if __name__ == "__main__":
    test_alias_detection()
