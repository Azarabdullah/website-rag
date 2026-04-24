

🌐 Website RAG
A command-line AI tool that scrapes any website and lets you ask questions about its content — powered by free LLMs via OpenRouter.


-------------------------------------------------------------------------------------------------------------------------------------------------------------


🚀 What It Does

Paste any URL → it scrapes the content
Ask questions about that website in plain English
AI answers using only the scraped content (no hallucination)
Automatically falls back to next model if one fails



--------------------------------------------------------------------------------------------------------------------------------------------------------------


🛠️ Tech Stack
ToolPurposePythonCore languageBeautifulSoup4Web scrapingOpenRouter APIFree LLM accesspython-dotenvAPI key managementOpenAI SDKAPI client


--------------------------------------------------------------------------------------------------------------------------------------------------------------
⚙️ Setup
1. Clone the repo
bashgit clone https://github.com/Azarabdullah/website-rag.git
cd website-rag
2. Create virtual environment
bashpython -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
3. Install dependencies
bashpython -m pip install requests beautifulsoup4 python-dotenv openai
4. Add your API key
Create a .env file in the project root:
OPENROUTER_API_KEY=sk-or-your-key-here
Get a free key at 👉 openrouter.ai/keys
5. Run it
bashpython rag.py
--------------------------------------------------------------------------------------------------------------------------------------------------------------
💬 Usage
=== WEBSITE RAG ===
Commands: change | exit

Enter URL: https://en.wikipedia.org/wiki/Python_(programming_language)
⏳ Scraping...
✅ Ready — 12 chunks loaded

Ask a question: What is Python?
🤖 Thinking...

[google/gemma-3-4b-it:free]
Python is a high-level, general-purpose programming language known for its
clear syntax and readability...
Commands
CommandActionAny questionAsk about the current websitechangeSwitch to a different URLexitQuit the program

🤖 Models Used (Free)
The app tries these models in order, falling back if one fails or is rate-limited:

openrouter/free — auto-selects best available free model
microsoft/phi-4-reasoning:free
deepseek/deepseek-r1:free
qwen/qwen3-8b:free
google/gemma-3-4b-it:free
google/gemma-3-27b-it:free
meta-llama/llama-3.3-70b-instruct:free




--------------------------------------------------------------------------------------------------------------------------------------------------------------

📁 Project Structure
website-rag/
├── rag.py          # Main application
├── .env            # API key (not uploaded to GitHub)
├── .gitignore      # Ignores .env and venv
└── README.md       # You are here



--------------------------------------------------------------------------------------------------------------------------------------------------------------
⚠️ Rate Limits
Free OpenRouter models allow:

20 requests/minute
200 requests/day

If you hit limits, wait 1-2 minutes and try again, or sign up for OpenRouter credits.




--------------------------------------------------------------------------------------------------------------------------------------------------------------
🙋 Author
Azar Abdullah
GitHub: @Azarabdullah

📄 License
Do whatever you want with this — just bring your own API key. 🔑
