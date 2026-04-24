import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# ── Load API key ──────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)
MODELS = [
    "openrouter/free",
    "microsoft/phi-4-reasoning:free",
    "deepseek/deepseek-r1:free",
    "qwen/qwen3-8b:free",
    "google/gemma-3-4b-it:free",
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
]
# ── Scrape & chunk website ────────────────────────────────────
def scrape(url: str) -> str:
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)
        return text
    except Exception as e:
        return f"ERROR scraping: {e}"


def chunk(text: str, size: int = 1500, overlap: int = 200) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def top_chunks(query: str, chunks: list[str], k: int = 3) -> str:
    q = query.lower()
    scored = sorted(chunks, key=lambda c: sum(w in c.lower() for w in q.split()), reverse=True)
    return "\n\n---\n\n".join(scored[:k])


# ── Ask LLM ──────────────────────────────────────────────────
def ask(query: str, context: str) -> str:
    prompt = (
        f"Use ONLY the context below to answer the question.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {query}\n\nANSWER:"
    )
    for model in MODELS:
        try:
            res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
            )
            return f"[{model}]\n{res.choices[0].message.content.strip()}"
        except Exception as e:
            print(f"  ⚠ {model} failed: {e}")
    return "❌ All models failed. Check your API key."


# ── Main loop ─────────────────────────────────────────────────
def main():
    print("\n=== WEBSITE RAG ===")
    print("Commands: change | exit\n")

    url = input("Enter URL: ").strip()
    print("⏳ Scraping...")
    text = scrape(url)
    if text.startswith("ERROR"):
        print(text)
        return
    chunks = chunk(text)
    print(f"✅ Ready — {len(chunks)} chunks from {url}\n")

    while True:
        query = input("Ask a question: ").strip()
        if not query:
            continue
        if query.lower() == "exit":
            print("Bye!")
            break
        if query.lower() == "change":
            url = input("Enter new URL: ").strip()
            print("⏳ Scraping...")
            text = scrape(url)
            if text.startswith("ERROR"):
                print(text)
                continue
            chunks = chunk(text)
            print(f"✅ Ready — {len(chunks)} chunks from {url}\n")
            continue

        context = top_chunks(query, chunks)
        print("\n🤖👾 Thinking...\n")
        answer = ask(query, context)
        print(answer)
        print()


if __name__ == "__main__":
    main()