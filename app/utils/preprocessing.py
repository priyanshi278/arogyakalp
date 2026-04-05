import string

def preprocess_text(text: str) -> str:
    """
    Trim whitespace. (Aggressive preprocessing disabled to preserve NER accuracy)
    """
    if not text:
        return ""
    
    return text.strip()
