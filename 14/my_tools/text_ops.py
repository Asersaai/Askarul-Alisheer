def capitalize_words(text):
    """Capitalize the first letter of every word."""
    return " ".join(word.capitalize() for word in text.split())

def count_char(text, char):
    """Count how many times a character occurs in a string."""
    return text.count(char)
