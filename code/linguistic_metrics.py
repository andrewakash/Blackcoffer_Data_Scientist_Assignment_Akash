import os
import re

# -------------------------------
# Basic word cleaning
# -------------------------------
def get_words(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = text.split()
    return words


# -------------------------------
# Syllable count per word
# -------------------------------
def count_syllables(word):
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

    if word.endswith(("es", "ed")):
        count -= 1

    return max(1, count)


# -------------------------------
# Personal pronouns
# -------------------------------
def count_personal_pronouns(text):
    pronouns = re.findall(r'\b(i|we|my|ours|us)\b', text, re.IGNORECASE)
    return len(pronouns)


# -------------------------------
# Linguistic Metrics
# -------------------------------
def linguistic_metrics(text):
    words = get_words(text)
    total_words = len(words)

    total_syllables = sum(count_syllables(word) for word in words)
    syllables_per_word = total_syllables / total_words if total_words else 0

    total_characters = sum(len(word) for word in words)
    avg_word_length = total_characters / total_words if total_words else 0

    pronoun_count = count_personal_pronouns(text)

    return {
        "Word Count": total_words,
        "Syllables Per Word": syllables_per_word,
        "Personal Pronouns": pronoun_count,
        "Average Word Length": avg_word_length
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

    results = linguistic_metrics(text)

    for key, value in results.items():
        print(f"{key}: {round(value, 4)}")
