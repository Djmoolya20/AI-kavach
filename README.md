# 🛡️ AI-Kavach — LLM Security Proxy & SIEM Dashboard

AI-Kavach is a real-time AI security system that intercepts and blocks prompt injection attacks, jailbreak attempts, and data exfiltration before they reach an LLM-powered customer support agent. It features a live SIEM-style dashboard for monitoring all incoming traffic.

---

## 🎯 What It Does

Most AI chatbots are vulnerable to prompt injection — users can trick them into leaking system instructions, bypassing rules, or giving unauthorized discounts. AI-Kavach sits in front of the LLM as a security proxy and blocks malicious prompts before they ever reach the model.

**Result: 10/10 attack types blocked in live testing.**

---

## 🏗️ Architecture

```
User Prompt
    │
    ▼
┌─────────────────────────────┐
│   FastAPI Security Proxy    │  ← backend/main.py
│   (ws://localhost:8000)     │
│                             │
│  ┌───────────────────────┐  │
│  │   security_core.py    │  │  ← Vector similarity + regex filters
│  │  ChromaDB + ML model  │  │  ← sentence-transformers embeddings
│  └───────────────────────┘  │
└─────────────────────────────┘
    │               │
    ▼               ▼
Blocked ✋      Safe ✅
    │               │
    │               ▼ (simulator calls agent directly)
    │          LLM Agent (Groq)
    │               │
    │               ▼
    │          Customer Reply
    │               │
    └───────┬───────┘
            ▼
┌─────────────────────────────┐
│   Next.js SIEM Dashboard    │  ← frontend/app/page.js
│   (http://localhost:3000)   │  ← Live WebSocket feed
└─────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Groq API key](https://console.groq.com)

---

### 1. Clone the Repository

```bash
git clone https://github.com/Djmoolya20/AI-kavach.git
cd AI-kavach
```

---

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder:

```
GROQ_API_KEY=your_groq_api_key_here
```

Seed the vector database (first time only):

```bash
python security_core.py
```

Start the backend server:

```bash
python -m uvicorn main:app --reload
```

Backend runs at: **http://localhost:8000**
Health check: **http://localhost:8000/health**

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Dashboard runs at: **http://localhost:3000**

---

### 4. Run the Simulator

In a third terminal:

```bash
cd simulator
pip install -r simulator_requirements.txt
```

Create a `.env` file inside the `simulator/` folder (one time only):

```
GROQ_API_KEY=your_groq_api_key_here
```

Then run attack simulations directly every time — no need to set the key again:

```bash
# Safe baseline queries (control group)
python test_a_safe_query.py --demo

# Jailbreak & prompt injection attacks
python test_b_jailbreak.py --demo

# Data exfiltration attempts
python test_c_data_exfiltration.py --demo
```

Watch the dashboard update in real time as attacks are intercepted.

---

## 🔒 Security Features

| Attack Type | Detection Method | Result |
|---|---|---|
| Prompt injection (`ignore all previous instructions`) | Keyword regex filter | BLOCKED |
| DAN / role-play bypass | Vector similarity search | BLOCKED |
| Fake admin / developer authority | Vector similarity search | BLOCKED |
| System prompt extraction | Vector similarity search | BLOCKED |
| Fictional framing bypass | Vector similarity search | BLOCKED |
| Data exfiltration attempts | Vector similarity search | BLOCKED |
| Hypothetical permission framing | Vector similarity search | BLOCKED |
| Format-trick extraction | Vector similarity search | BLOCKED |

**Detection rate: 10/10 attack types neutralized**

---

## 📁 Project Structure

```
AI-kavach/
├── backend/
│   ├── main.py               # FastAPI server, WebSocket proxy
│   ├── security_core.py      # ML detection engine (ChromaDB + embeddings)
│   ├── schemas.py            # Pydantic data models
│   ├── threshold_calibration.py
│   └── requirements.txt
│
├── frontend/
│   └── app/
│       ├── page.js           # SIEM dashboard (React + WebSocket)
│       ├── layout.js
│       └── globals.css
│
└── simulator/
    ├── agent.py              # Mock LLM customer support agent (Groq)
    ├── proxy_client.py       # WebSocket client routing through proxy
    ├── test_a_safe_query.py  # Safe baseline tests
    ├── test_b_jailbreak.py   # Jailbreak attack tests
    ├── test_c_data_exfiltration.py
    └── simulator_requirements.txt
```

---

## 🖥️ Dashboard Features

- **Live Monitor Feed** — Real-time WebSocket stream of all incoming requests
- **Intercepted Attacks** — Filtered view of blocked threats only
- **Full Security Logs** — Complete audit trail
- **Guardrail Rules** — The 6 policy rules protecting the ShopBot agent
- **Forensic Inspector** — Click any event to see full details (IP, query, risk score, violated rule)
- **Traffic Simulator** — Inject safe or threat traffic directly from the UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Security Proxy | FastAPI, WebSockets |
| ML Detection | sentence-transformers, ChromaDB |
| LLM Agent | Groq (llama3) |
| Dashboard | Next.js 14, Tailwind CSS |
| Simulator | Python, websockets |

---

## 👥 Team

Built at a hackathon in 4 days by a 4-member team:

| Role | Member |
|---|---|
| **Member 1** — Backend Engineer (FastAPI proxy, WebSocket) | Aadit Deshmukh |
| **Member 2** — Security Engineer (ML detection, ChromaDB) | Amey Padwal |
| **Member 3** — Frontend Developer (Next.js SIEM dashboard) | Mayuresh Panhalkar |
| **Member 4** — Tester / Presenter (Simulator, attack scripts) | Dheeraj Moolya |