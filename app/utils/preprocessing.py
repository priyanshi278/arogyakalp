import string

def preprocess_text(text: str) -> str:
    """
    Lowercase text and remove punctuation.
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    
    return text.strip()
