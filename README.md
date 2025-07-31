# 🤖 Grok Chatbot with Persistent Memory (Mem0.ai)

Welcome to the **Grok Chatbot** — a Python-based conversational AI built with **Streamlit**, powered by the **Groq LLM**, and enhanced with **persistent memory** via [Mem0.ai](https://app.mem0.ai/dashboard/get-started).  
This project delivers an intelligent, personalized chat experience that remembers user-specific details (like preferences) across sessions.

---

## 🚀 Features

- **🧠 Intelligent Conversations**  
  Powered by `llama3-8b-8192` from Groq for fast, context-aware replies.

- **🗃️ Persistent Memory (Mem0.ai)**  
  Cloud memory to store user facts like “I like Python” across restarts.

- **💡 Enhanced Streamlit UI**
  - Scrollable Chat Window
  - Fixed Chat Input Bar
  - Custom Avatars (🧑‍💻 User / 🤖 Assistant)
  - Chat History Export (📦 JSON)
  - Memory Viewer (Sidebar)
  - Token Count Display
  - Feedback Buttons (👍 / 👎)
  - Clear Chat Option

- **🛠️ Robust Error Handling**  
  Handles Groq/Mem0 errors with messages and logs.

- **🔐 Secure Environment Management**  
  Uses `.env` for loading API keys safely.

---
## Screenshot:
<img width="1359" height="602" alt="image" src="https://github.com/user-attachments/assets/ee081ccd-5cd8-47d0-bc7e-9968ecf342c4" />

---

## 🎯 Why This Project?

This chatbot explores the synergy between **Groq’s ultra-fast LLMs** and **Mem0’s innovative memory infrastructure**.  
It’s designed to be:
- Dev-friendly
- Memory-aware
- Ready to inspire your next AI project

Perfect for:
- AI learners
- Streamlit devs
- Anyone building memory-enhanced agents

---

## 🧰 Getting Started

### ✅ Prerequisites

- Python **≤ 3.11** (Mem0 not supported on Python 3.12+)
- Virtual Environment (recommended)
- API Keys:
  - Groq: [console.groq.com](https://console.groq.com)
  - Mem0.ai: [mem0.ai dashboard](https://app.mem0.ai/dashboard/get-started)

---

### ⚙️ Installation

```bash
# 1. Clone the Repo
git clone https://github.com/your-username/grok-chatbot.git
cd grok-chatbot

# 2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Set Up Environment Variables
echo "GROQ_API_KEY=your_groq_api_key" >> .env
echo "MEM0_API_KEY=your_mem0_api_key" >> .env
````

---

### ▶️ Run the App

```bash
streamlit run app.py
```

Then open: [http://localhost:8501](http://localhost:8501)

---

## 💬 Example Interaction

```text
You: My name is Alex, and I like coding in Python.
Bot: Nice to meet you, Alex! Python's a great language.
```

Action: Click **"Check Stored Memories"** in the sidebar.

```text
You: What's my name?
Bot: You’re Alex, right? Still coding in Python?
```

Action: Export chat history or give feedback with 👍 / 👎

---

## 📁 Project Structure

```
grok-chatbot/
├── app.py              # Main Streamlit chatbot app
├── requirements.txt    # Dependencies
├── .env                # Environment variables (not committed)
├── .gitignore          # Files to ignore in git
└── README.md           # Project documentation
```

---

## 📦 Dependencies

Listed in `requirements.txt`:

* `streamlit==1.36.0`
* `groq==0.9.0`
* `mem0ai==0.1.115`
* `python-dotenv==1.0.1`
* `tiktoken==0.7.0`

---

## 🛠️ Debugging Tips

| Problem                 | Fix                                                                 |
| ----------------------- | ------------------------------------------------------------------- |
| Memory not saving       | Check `.env` and confirm `MEM0_API_KEY` is valid via Mem0 dashboard |
| API Errors              | Shown in UI and logs; check Groq/Mem0 usage dashboards              |
| Python Version Error    | Must use Python 3.11 or earlier                                     |
| Conda Environment Issue | Run `conda deactivate` before launching app                         |

---

## Ideas for improvements:

* Add Speech-to-Text input (via `speech_recognition`)
* Add a custom UI theme with CSS
* Store feedback responses in a database
* Support multiple users via `user_id` field



---

## Acknowledgments

* **Groq** – blazing-fast inference
* **Mem0.ai** – persistent memory infrastructure
* **Streamlit** – rapid web UI framework
* **Python community** – for all the tools & support

---

⭐ **Star this repo if you found it useful!**
Let’s build smarter memory-powered chatbots together 🚀

```

```
