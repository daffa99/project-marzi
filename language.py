from textblob import TextBlob


def is_english(text):
    text_blob = TextBlob(text)
    detected_lang = text_blob.detect_language()
    if detected_lang == "en":
        return True
    else:
        return False