# intent.py
# Full-sentence understanding for Hinglish + Hindi + Urdu
# Deterministic NLU (NO AI, NO CLOUD)

import re


# ---------- NORMALIZATION ----------
def normalize_text(text: str) -> str:
    text = text.lower().strip()

    replacements = {
        # Roman Hindi / Hinglish
        "bijli": "light",
        "lाइट": "light",
        "light": "light",
        "fan": "fan",
        "pankha": "fan",
        "paani": "water",
        "nal": "water",
        "room": "room",
        "kamra": "room",
        "hostel": "hostel",

        # Hindi (Devanagari)
        "बिजली": "light",
        "लाइट": "light",
        "पंखा": "fan",
        "पानी": "water",
        "कमरा": "room",
        "होस्टल": "hostel",
        "नहीं": "not",
        "नही": "not",
        "चल": "work",
        "आ": "come",

        # Urdu
        "بجلی": "light",
        "لائٹ": "light",
        "پنکھا": "fan",
        "پانی": "water",
        "کمرہ": "room",
        "ہاسٹل": "hostel",
        "نہیں": "not",

        # Common phrases
        "not working": "not_working",
        "nahi chal raha": "not_working",
        "kaam nahi kar raha": "not_working",
        "nahi aa rahi": "not_working",
        "band ho rahi": "not_working",
        "baar baar band": "fluctuating",
        "sometimes": "fluctuating",
        "kabhi kabhi": "fluctuating"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # clean extra spaces
    text = re.sub(r"\s+", " ", text)
    return text


# ---------- FULL SENTENCE PARSER ----------
def parse_issue(text: str) -> dict:
    text = normalize_text(text)

    issue = {
        "intent": "unknown",
        "issue_type": None,
        "severity": None,
        "location": None
    }

    # LOCATION
    if "room" in text:
        issue["location"] = "room"
    elif "hostel" in text:
        issue["location"] = "hostel"

    # ISSUE TYPE
    if "light" in text:
        issue["issue_type"] = "light"
    elif "fan" in text:
        issue["issue_type"] = "fan"
    elif "water" in text:
        issue["issue_type"] = "water"

    # SEVERITY
    if "not_working" in text:
        issue["severity"] = "not_working"
    elif "fluctuating" in text:
        issue["severity"] = "fluctuating"

    # FINAL INTENT DECISION
    if issue["issue_type"] and issue["location"]:
        issue["intent"] = "hostel"

    return issue


# ---------- MAIN ENTRY ----------
def detect_intent(text: str) -> dict:
    """
    Returns structured understanding, not just intent string
    """
    return parse_issue(text)


# ---------- LOCAL TEST ----------
if __name__ == "__main__":
    tests = [
        "mere room ki light nahi aa rahi",
        "میرے روم کی بجلی نہیں آ رہی ہے",
        "hostel ke kamre me fan kabhi kabhi band ho jata hai",
        "मेरे कमरे में पानी नहीं आ रहा"
    ]

    for t in tests:
        print("Input:", t)
        print("Parsed:", detect_intent(t))
        print("-" * 50)
