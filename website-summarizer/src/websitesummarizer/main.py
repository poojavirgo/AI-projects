from dotenv import load_dotenv
from httpx2 import URL
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def fetch_website_text(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    return soup.get_text(separator=" ", strip=True)


def summarize_website(text):
    messages = [
        {
            "role": "system",
            "content": "You summarize websites."
        },
        {
            "role": "user",
            "content": f"Summarize this website:\n{text}"
        }
    ]

    response = client.chat.completions.create(
        model="llama3.2",
        messages=messages
    )

    return response.choices[0].message.content


url = input("Enter website URL: ")

try:
    website_text = fetch_website_text(url)

    summary = summarize_website(website_text)

    print("\n--- SUMMARY ---\n")
    print(summary)


except Exception as e:
    print(f"Error: {e}")