# 🛠️ AI IT Helpdesk Agent

A small end-to-end AI IT Helpdesk prototype for the TN Skill project.

The project demonstrates the required **Agent + RAG + Tools** architecture:

- **Agent:** Gemini decides how to respond and whether to use tools.
- **RAG:** A local knowledge base is embedded with Gemini and searched using cosine similarity.
- **Tools:** Internet connectivity check, system information, and support-ticket creation.
- **Memory:** Streamlit keeps the conversation history for the current session.
- **Tickets:** SQLite stores locally created demo support tickets.

## Architecture

```text
                User
                 │
                 ▼
          Streamlit Chat UI
                 │
                 ▼
          AI IT Helpdesk Agent
                 │
        ┌────────┼─────────┐
        │        │         │
        ▼        ▼         ▼
       RAG      Tools     LLM
        │        │         │
        ▼        ▼         │
   Knowledge   Python      │
    Base       Functions   │
        │        │         │
        └────────┴─────────┘
                 │
                 ▼
            Final Answer
```

## Project Structure

```text
ai_it_helpdesk_agent/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── knowledge_base/
│   ├── wifi_troubleshooting.md
│   ├── printer_troubleshooting.md
│   ├── vpn_troubleshooting.md
│   ├── password_reset.md
│   ├── email_troubleshooting.md
│   ├── slow_computer.md
│   ├── blue_screen.md
│   ├── software_installation.md
│   ├── keyboard_mouse.md
│   ├── network_slow.md
│   └── login_troubleshooting.md
│
├── src/
│   ├── agent.py
│   ├── config.py
│   ├── rag.py
│   ├── tools.py
│   └── __init__.py
│
├── scripts/
│   └── build_index.py
│
├── tests/
│   └── test_rag.py
│
└── data/
    └── .gitkeep
```

## 1. Prerequisites

- Python 3.10+
- A Gemini API key
- Git

Google's current Gemini Python SDK is `google-genai`.

## 2. Setup on Windows

> **API key safety:** The key shared with ChatGPT is not embedded in this project or ZIP. Put your key only in `.env`. Because a live key was pasted into chat, rotate/revoke it before publishing the repository and use the replacement key in `.env`.


Open PowerShell inside the project folder:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create the local environment file:

```powershell
copy .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

with your real API key.

**Never commit `.env` to GitHub.**

## 3. Build the RAG index

Run:

```powershell
python scripts\build_index.py
```

Expected result:

```text
Built RAG index for 11 documents.
Saved to: data/embeddings.json
```

The generated vector index is ignored by Git because it is a local runtime artifact.

## 4. Run the app

```powershell
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## 5. Demo Questions

Try these:

```text
My Wi-Fi is connected but I cannot access the internet.

My laptop is very slow. Can you diagnose it?

My printer is offline.

I cannot connect to the VPN.

My keyboard is not working.

My Windows PC keeps showing a blue screen.

My network is very slow.

Create a support ticket for my Wi-Fi issue with High priority.
```

## 6. What counts as Agent + RAG + Tools here?

### RAG
The app retrieves the most relevant troubleshooting articles before sending the request to Gemini.

### Agent
Gemini receives the problem, conversation history, retrieved evidence, and tool definitions. It decides how to respond and whether a tool is useful.

### Tools
The model can call:

```text
check_internet_connection()
get_system_info()
create_support_ticket(issue, priority)
```

The Python application executes the function and returns its result to the model.

## 7. Security

Do not hard-code API keys in Python.

The repository contains `.env.example`, not the real secret.

Also do not commit:

```text
.env
data/helpdesk.db
data/embeddings.json
```

These paths are covered by `.gitignore`.

## 8. GitHub Commands

After testing the project:

```powershell
git init
git add .
git status
git commit -m "Add AI IT Helpdesk Agent"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Before the first `git push`, verify that `.env` does not appear in:

```powershell
git status
```

## 9. Limitations

This is a student prototype, not an enterprise helpdesk system.

- Ticket storage is local SQLite.
- Internet checks depend on the local machine's network.
- The knowledge base is intentionally small.
- There is no authentication or role management.
- Tool actions are designed only for a safe classroom demo.
