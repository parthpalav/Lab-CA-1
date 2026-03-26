def search(text, keyword):
    if keyword.lower() in text.lower():
        return f"Found '{keyword}' in document"
    else:
        return f"'{keyword}' not found"