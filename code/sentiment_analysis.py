import os
import re

# -------------------------------
# Load Stop Words (reuse Step 2)
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
# Clean Text (reuse Step 2)
# -------------------------------
def clean_text(text, stop_words):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = text.split()
    cleaned_words = [w for w in words if w not in stop_words]
    return cleaned_words


# -------------------------------
# Load Master Dictionary
# -------------------------------
def load_master_dictionary(file_path):
    words = set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            words.add(line.strip().lower())
    return words


# -------------------------------
# Sentiment Analysis
# -------------------------------
def sentiment_scores(cleaned_words, positive_words, negative_words):
    positive_score = 0
    negative_score = 0

    for word in cleaned_words:
        if word in positive_words:
            positive_score += 1
        elif word in negative_words:
            negative_score += 1

    polarity_score = (positive_score - negative_score) / (
        (positive_score + negative_score) + 0.000001
    )

    subjectivity_score = (positive_score + negative_score) / (
        len(cleaned_words) + 0.000001
    )

    return positive_score, negative_score, polarity_score, subjectivity_score


# -------------------------------
# MAIN EXECUTION (TEST)
# -------------------------------
if __name__ == "__main__":

    stopwords_folder = "stopwords_folder"
    articles_folder = "ExtractedArticles"
    master_dict_folder = "MasterDictionary"

    # Load resources
    stop_words = load_stopwords(stopwords_folder)
    positive_words = load_master_dictionary(
        os.path.join(master_dict_folder, "positive-words.txt")
    )
    negative_words = load_master_dictionary(
        os.path.join(master_dict_folder, "negative-words.txt")
    )

    # Test with one article
    sample_file = os.listdir(articles_folder)[0]
    sample_path = os.path.join(articles_folder, sample_file)

    with open(sample_path, 'r', encoding='utf-8', errors='ignore') as f:
        article_text = f.read()

    cleaned_words = clean_text(article_text, stop_words)

    pos, neg, polarity, subjectivity = sentiment_scores(
        cleaned_words, positive_words, negative_words
    )

    print("Positive Score:", pos)
    print("Negative Score:", neg)
    print("Polarity Score:", round(polarity, 4))
    print("Subjectivity Score:", round(subjectivity, 4))
