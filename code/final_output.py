import os
import re
import pandas as pd

# -------------------------------
# Utility functions (REUSED)
# -------------------------------
def load_stopwords(folder):
    stop_words = set()
    for file in os.listdir(folder):
        with open(os.path.join(folder, file), 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stop_words.add(line.strip().lower())
    return stop_words


def load_dictionary(file_path):
    words = set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            words.add(line.strip().lower())
    return words


def clean_text(text, stop_words):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = text.split()
    return [w for w in words if w not in stop_words]


def count_sentences(text):
    sentences = re.split(r'[.!?]', text)
    return len([s for s in sentences if s.strip()])


def count_syllables(word):
    vowels = "aeiou"
    count = 0
    prev = False
    for char in word:
        if char in vowels:
            if not prev:
                count += 1
            prev = True
        else:
            prev = False
    if word.endswith(("es", "ed")):
        count -= 1
    return max(1, count)


def count_pronouns(text):
    return len(re.findall(r'\b(i|we|my|ours|us)\b', text, re.I))


# -------------------------------
# MAIN EXECUTION
# -------------------------------
input_df = pd.read_excel("Input.xlsx")

stop_words = load_stopwords("stopwords_folder")
positive_words = load_dictionary("MasterDictionary/positive-words.txt")
negative_words = load_dictionary("MasterDictionary/negative-words.txt")

results = []

for _, row in input_df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]

    file_path = f"ExtractedArticles/{url_id}.txt"

    if not os.path.exists(file_path):
        continue

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    words = clean_text(text, stop_words)
    total_words = len(words)

    pos = sum(1 for w in words if w in positive_words)
    neg = sum(1 for w in words if w in negative_words)

    polarity = (pos - neg) / ((pos + neg) + 0.000001)
    subjectivity = (pos + neg) / (total_words + 0.000001)

    sentences = count_sentences(text)
    avg_sentence_len = total_words / sentences if sentences else 0

    complex_words = sum(1 for w in words if count_syllables(w) > 2)
    percent_complex = complex_words / total_words if total_words else 0
    fog_index = 0.4 * (avg_sentence_len + percent_complex)

    syllables_per_word = sum(count_syllables(w) for w in words) / total_words if total_words else 0
    avg_word_len = sum(len(w) for w in words) / total_words if total_words else 0
    pronouns = count_pronouns(text)

    results.append([
        url_id, url, pos, neg, polarity, subjectivity,
        avg_sentence_len, percent_complex, fog_index,
        avg_sentence_len, complex_words, total_words,
        syllables_per_word, pronouns, avg_word_len
    ])

# -------------------------------
# SAVE OUTPUT
# -------------------------------
columns = [
    "URL_ID", "URL",
    "POSITIVE SCORE", "NEGATIVE SCORE",
    "POLARITY SCORE", "SUBJECTIVITY SCORE",
    "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS",
    "FOG INDEX", "AVG NUMBER OF WORDS PER SENTENCE",
    "COMPLEX WORD COUNT", "WORD COUNT",
    "SYLLABLE PER WORD", "PERSONAL PRONOUNS",
    "AVG WORD LENGTH"
]

output_df = pd.DataFrame(results, columns=columns)
output_df.to_excel("Final_Output.xlsx", index=False)

print("✅ Final_Output.xlsx generated successfully")
