# 🎥 FlickMind – AI Cinema Intelligence

A project built with **Weaviate Agents** (Query Agent + Transformation Agent) and **Streamlit**.  
Domain: Movies / TV Series / Directors.

---

## Architecture

```
flickmind/
├── data/
│   └── load_data.py             # Loads 3 collections into Weaviate Cloud
├── agents/
│   ├── __init__.py              # Python package
│   ├── query_agent.py           # Query Agent – natural language Q&A
│   └── transformation_agent.py # Transformation Agent – AI data enrichment
├── ui/
│   └── app.py                   # Streamlit interface (FlickMind)
├── docs/
│   └── report.md                # Technical report
├── .env.example                 # Environment variable template
├── requirements.txt
└── README.md
```

### Weaviate Collections

| Collection  | Items | Key properties                                                |
|-------------|-------|---------------------------------------------------------------|
| `Movies`    | 12    | title, year, genre, director, rating, plot, duration, awards  |
| `TVSeries`  | 10    | title, creator, seasons, episodes, network, status, rating    |
| `Directors` | 6     | name, nationality, style, biography, notable_works, awards    |

---

## Installation

### 1. Requirements
- Python 3.11+  
- Weaviate Cloud account (free Sandbox): https://console.weaviate.cloud  
- OpenAI API key: https://platform.openai.com

### 2. Unzip and navigate

```bash
cd flickmind
```

### 3. Virtual environment and dependencies

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Environment variables

```bash
cp .env.example .env
```

Edit `.env`:
```
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your-weaviate-api-key
OPENAI_API_KEY=sk-...
```

---

## Running

### Step 1: Load data (once)

```bash
python data/load_data.py
```

### Step 2: Launch FlickMind UI

```bash
streamlit run ui/app.py
```

Open your browser at: `http://localhost:8501`

---

## Features

### 🎥 Query Agent (Chat Interface)
Type any question or click an example in the sidebar.  
Conversation history is automatically passed to the agent for follow-up questions.

**Example queries:**

| Type | Example |
|------|---------|
| Semantic search | `Recommend a high-rated crime film` |
| Multi-collection | `What is Nolan's style and which of his films are in the database?` |
| Follow-up | `Which of those won an Oscar for visual effects?` |
| Aggregation | `How many HBO series have a rating above 9.0?` |
| Mood-based | `I want something dark and psychologically intense` |

### 🎭 Mood Search
Click a mood card on the main page to instantly fire a vibe-based query:
- 🌑 Dark & Intense
- 😂 Fun & Light
- 🤯 Mind-Bending
- ❤️ Romantic
- 🚀 Action & Epic
- 🏆 Award-Winning

### 🔄 Transformation Agent (Sidebar)
1. Click **🎥 ai_summary** – adds a 2-3 sentence summary to every movie  
2. Click **📺 ai_tags** – adds thematic tags to every TV series  
3. Wait for completion (~1-3 min) – results shown in an expandable panel

### 📥 Export Conversation
After chatting, use the **Export conversation** panel at the bottom to download the full conversation as a `.txt` file.

> ⚠️ **Warning:** Transformation Agent modifies data in-place.  
> Use only on test collections!

---

## Technologies

- **Weaviate Cloud** – vector database  
- **Weaviate Query Agent** – natural language → Weaviate queries  
- **Weaviate Transformation Agent** – AI data enrichment  
- **OpenAI text-embedding-ada-002** – vectorization  
- **Streamlit** – user interface  
- **Python 3.11+**
