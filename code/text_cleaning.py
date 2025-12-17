import os
import re
# import nltk
# from nltk.tokenize import word_tokenize

# # Download tokenizer (only first time)
# nltk.download('punkt')

# -------------------------------
# STEP 2.1: Load Stop Words
# -------------------------------
def load_stopwords(stopwords_folder):
    stop_words = set()

    for file in os.listdir(stopwords_folder):
        file_path = os.path.join(stopwords_folder, file)

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stop_words.add(line.strip().lower())

    return stop_words


# -------------------------------
# STEP 2.2–2.5: Clean Text
# -------------------------------
def clean_text(text, stop_words):
    text = text.lower()                     # lowercase
    text = re.sub(r'[^a-z\s]', ' ', text)   # remove punctuation & numbers
    words = text.split()                    # tokenize
    cleaned_words = [w for w in words if w not in stop_words]
    return cleaned_words


    # Tokenization
    words = text.split()


    # Remove stop words
    cleaned_words = [word for word in words if word not in stop_words]

    return cleaned_words


# -------------------------------
# MAIN EXECUTION (TEST)
# -------------------------------
if __name__ == "__main__":

    # ✅ IMPORTANT: match folder name exactly
    stopwords_folder = "stopwords_folder"
    articles_folder = "ExtractedArticles"

    # Load stop words
    stop_words = load_stopwords(stopwords_folder)
    print("Stop words loaded:", len(stop_words))

    # Pick ONE article to test
    sample_file = os.listdir(articles_folder)[0]
    sample_path = os.path.join(articles_folder, sample_file)

    with open(sample_path, 'r', encoding='utf-8', errors='ignore') as f:
        article_text = f.read()

    cleaned_words = clean_text(article_text, stop_words)

    print("\nSample cleaned words:")
    print(cleaned_words[:30])

    print("\nTotal cleaned word count:", len(cleaned_words))
