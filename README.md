<div align="center">

# 🎥 FlickMind

### AI-Powered Cinema Intelligence Assistant

*Ask anything about movies, TV series, and directors — powered by Weaviate Agents and OpenAI*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Weaviate](https://img.shields.io/badge/Weaviate-Cloud-green?style=flat-square)](https://weaviate.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## What is FlickMind?

FlickMind is an intelligent cinema assistant that lets you search and explore a curated database of movies, TV series, and directors using **natural language**. Ask complex questions, follow up on answers, and let AI enrich the data automatically — all through a sleek Streamlit interface.

Built on top of **Weaviate Agents** (Query Agent + Transformation Agent), FlickMind demonstrates how vector databases and LLMs can power real conversational search experiences.

---

## Features

### 🔍 Natural Language Q&A
Ask anything in plain English. The Query Agent searches across all three collections and composes a coherent answer with specific details.
```
"Recommend a psychological thriller with a rating above 8"
"What is Nolan's directing style and which of his films are in the database?"
"How many HBO series have a rating above 9.0?"
"Which of those won an Oscar for visual effects?"   ← follow-up, context is remembered
```

### 🎭 Mood Search
Six one-click mood cards that instantly fire a vibe-based query:

| Mood | Vibe |
|------|------|
| 🌑 Dark & Intense | Crime, psychological thriller, dark drama |
| 😂 Fun & Light | Comedy, feel-good, lighthearted |
| 🤯 Mind-Bending | Twist endings, philosophical, surreal |
| ❤️ Romantic | Love stories, emotional, heartwarming |
| 🚀 Action & Epic | Blockbuster, adventure, spectacle |
| 🏆 Award-Winning | Oscars, critically acclaimed, masterpieces |

### 🔄 AI Data Enrichment (Transformation Agent)
Enrich your database on-demand with AI-generated properties:
- **`ai_summary`** — a 2-3 sentence cinematic summary for every movie
- **`ai_tags`** — thematic tags for every TV series (e.g. `slow-burn`, `binge-worthy`, `mind-bending`)

### 💬 Conversation Memory
Follow-up questions work naturally — the last few exchanges are always passed as context to the agent.

### 📥 Export Conversations
Download your full chat session as a `.txt` file with one click.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Vector Database | [Weaviate Cloud](https://console.weaviate.cloud) |
| Query Agent | Weaviate QueryAgent |
| Transformation Agent | Weaviate TransformationAgent |
| Embeddings | OpenAI `text-embedding-ada-002` |
| UI | [Streamlit](https://streamlit.io) |
| Language | Python 3.11+ |

---

## Database Schema

| Collection | Records | Key Properties |
|------------|---------|----------------|
| `Movies` | 12 | title, year, genre, director, rating, plot, duration, awards |
| `TVSeries` | 10 | title, creator, seasons, episodes, network, status, rating |
| `Directors` | 6 | name, nationality, style, biography, notable_works, awards |

---

## Getting Started

### Prerequisites
- Python 3.11+
- A free [Weaviate Cloud](https://console.weaviate.cloud) account
- An [OpenAI API key](https://platform.openai.com)

### 1. Clone the repo
```bash
git clone https://github.com/your-username/flickmind.git
cd flickmind
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```

Edit `.env`:
```env
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your-weaviate-api-key
OPENAI_API_KEY=sk-...
```

### 5. Load the data (once)
```bash
python data/load_data.py
```

### 6. Run the app
```bash
streamlit run ui/app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## Project Structure
```
flickmind/
├── data/
│   └── load_data.py              # Populates Weaviate with sample data
├── agents/
│   ├── query_agent.py            # Natural language Q&A
│   └── transformation_agent.py  # AI data enrichment
├── ui/
│   └── app.py                    # Streamlit frontend
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚠️ Notes

- The **Transformation Agent modifies data in-place** — use only on test/sandbox collections.
- The free Weaviate Sandbox expires after **14 days**. Re-run `load_data.py` after creating a new cluster.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ using Weaviate · Streamlit · OpenAI
</div>
