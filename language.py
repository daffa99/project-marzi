from textblob import TextBlob

# Check if the language is english or not
def is_english(text):
    text_blob = TextBlob(text)
    detected_lang = text_blob.detect_language()
    if detected_lang == "en":
        return True
    else:
        return False