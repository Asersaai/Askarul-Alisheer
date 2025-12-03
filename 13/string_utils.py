def capitalize_words(text: str):
    return " ".join(word.capitalize() for word in text.split())

def count_letters(text: str):
    return sum(1 for ch in text if ch.isalpha())
