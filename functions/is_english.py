import string


def is_english(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    if len(set(text.lower() + string.ascii_lowercase)) == len(string.ascii_lowercase):
        return True
    else:
        return False