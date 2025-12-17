import os
import re

# -------------------------------
# Sentence Count
# -------------------------------
def count_sentences(text):
    sentences = re.split(r'[.!?]', text)
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)


# -------------------------------
# Word Cleaning (basic)
# -------------------------------
def get_words(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = text.split()
    return words


# -------------------------------
# Syllable Count per Word
# -------------------------------
def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    prev_char = False

    for char in word:
        if char in vowels:
            if not prev_char:
                count += 1
            prev_char = True
        else:
            prev_char = False

    # Remove silent endings
    if word.endswith(("es", "ed")):
        count -= 1

    return max(1, count)


# -------------------------------
# Readability Metrics
# -------------------------------
def readability_metrics(text):
    sentences = count_sentences(text)
    words = get_words(text)

    total_words = len(words)
    complex_words = sum(1 for w in words if count_syllables(w) > 2)

    avg_sentence_length = total_words / sentences if sentences else 0
    percentage_complex_words = complex_words / total_words if total_words else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = avg_sentence_length

    return {
        "Average Sentence Length": avg_sentence_length,
        "Complex Word Count": complex_words,
        "Percentage of Complex Words": percentage_complex_words,
        "Fog Index": fog_index,
        "Average Words Per Sentence": avg_words_per_sentence
    }


# -------------------------------
# MAIN EXECUTION (TEST)
# -------------------------------
if __name__ == "__main__":

    articles_folder = "ExtractedArticles"
    sample_file = os.listdir(articles_folder)[0]
    sample_path = os.path.join(articles_folder, sample_file)

    with open(sample_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    results = readability_metrics(text)

    for key, value in results.items():
        print(f"{key}: {round(value, 4)}")
