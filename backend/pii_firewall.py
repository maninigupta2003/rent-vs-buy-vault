import re

# Simple but effective PII patterns (acceptable for 48h sprint)
PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "PHONE": r"\b\d{9,15}\b",
    "IBAN": r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b",
    "PASSPORT": r"\b[A-Z]\d{7,8}\b",
    "NAME": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"
}

def scrub_pii(text: str) -> str:
    sanitized = text
    for label, pattern in PII_PATTERNS.items():
        sanitized = re.sub(pattern, f"[REDACTED_{label}]", sanitized)
    return sanitized
