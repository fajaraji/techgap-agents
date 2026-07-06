import re

def sanitize_pii(text: str) -> str:
    """
    Redact Personally Identifiable Information (PII) from text.
    This fulfills the Zero-Trust / Context Hygiene requirement.
    """
    if not text:
        return text
    
    # Redact Emails
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text = re.sub(email_pattern, '[REDACTED_EMAIL]', text)
    
    # Redact Phone Numbers (Basic formats)
    phone_pattern = r'(\+\d{1,3}[-.\s]??)?\(?\d{3}\)?[-.\s]??\d{3}[-.\s]??\d{4}'
    text = re.sub(phone_pattern, '[REDACTED_PHONE]', text)
    
    # Redact GitHub Tokens or general secret tokens (heuristic)
    token_pattern = r'(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}'
    text = re.sub(token_pattern, '[REDACTED_GITHUB_TOKEN]', text)
    
    return text
