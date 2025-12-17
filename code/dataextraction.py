import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# 1️⃣ Read Input.xlsx
input_file = "Input.xlsx"
df = pd.read_excel(input_file)

# 2️⃣ Create output folder if not exists
output_folder = "ExtractedArticles"
os.makedirs(output_folder, exist_ok=True)

# 3️⃣ Loop through each URL
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    try:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0 Safari/537.36"
    }
        # 4️⃣ Request webpage
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # 5️⃣ Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 6️⃣ Extract Title
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        # 7️⃣ Extract Article Text
        article_text = ""

        # Find all paragraph tags
        paragraphs = soup.find_all('p')

        for p in paragraphs:
            article_text += p.get_text() + "\n"

        # 8️⃣ Save to text file
        file_path = os.path.join(output_folder, f"{url_id}.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(title + "\n\n")
            file.write(article_text)

        print(f"Saved article: {url_id}.txt")


    except Exception as e:
        print(f"Error processing URL_ID {url_id}: {e}")

