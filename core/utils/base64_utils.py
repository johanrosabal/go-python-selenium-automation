import base64

def encode_base64(text: str) -> str:
    """Encodes a string to base64."""
    if text is None:
        return ""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decode_base64(encoded_text: str) -> str:
    """Decodes a base64 string."""
    if encoded_text is None:
        return ""
    return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
