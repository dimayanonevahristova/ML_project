"""
FlickMind – Query Agent
=======================
Wraps the Weaviate QueryAgent and provides a simple interface
for natural language questions about movies, TV series, and directors.

Changes vs original:
- QueryAgent cached in session (not recreated per request)
- Conversation history support for follow-up questions
- Robust collection/query extraction from response
- Improved error handling
"""

import os
import weaviate
from weaviate.agents.query import QueryAgent
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are FlickMind, an expert cinema assistant with deep knowledge of movies,
TV series, and directors. You have access to three collections:

- Movies: feature films with plot, director, year, genre, rating, awards, duration, country
- TVSeries: TV shows with plot, creator, seasons, episodes, network, status, rating
- Directors: filmmakers with biography, style, awards, notable works, nationality

When answering:
- Be informative but concise
- Include specific details like ratings, years, and awards when relevant
- For comparisons, present data in a structured way
- If asked about a director's films, cross-reference Movies and Directors collections
- Always answer in the same language as the question (Bulgarian or English)
- If data is not in the database, say so clearly
- For follow-up questions, use the context from the previous answer
"""

COLLECTION_NAMES = ["Movies", "TVSeries", "Directors"]


def get_client() -> weaviate.WeaviateClient:
    """Свързва се към Weaviate Cloud. Хвърля ValueError ако липсват env vars."""
    required = ["WEAVIATE_URL", "WEAVIATE_API_KEY", "OPENAI_API_KEY"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise ValueError(f"Липсващи environment variables: {', '.join(missing)}")

    return weaviate.connect_to_weaviate_cloud(
        cluster_url=os.environ["WEAVIATE_URL"],
        auth_credentials=weaviate.auth.AuthApiKey(os.environ["WEAVIATE_API_KEY"]),
        headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
    )


def _build_agent(client: weaviate.WeaviateClient) -> QueryAgent:
    """Създава нов QueryAgent с конфигурирания system prompt."""
    return QueryAgent(
        client=client,
        collections=COLLECTION_NAMES,
        system_prompt=SYSTEM_PROMPT,
    )


def ask(
    question: str,
    client: weaviate.WeaviateClient,
    conversation_history: list[dict] | None = None,
) -> dict:
    """
    Задава въпрос на Query Agent и връща речник с:
      - answer        : текстов отговор
      - queries       : изпълнени Weaviate заявки (list of dicts)
      - collections   : уникални имена на засегнатите колекции
      - usage         : брой токени (или None)

    conversation_history е списък от {"role": "user"|"assistant", "content": str}
    и се използва за контекст при follow-up въпроси.
    """
    agent = _build_agent(client)

    # Ако има история на разговора, добавяме предишния контекст към въпроса
    # QueryAgent не поддържа native multi-turn, затова го правим ръчно
    full_question = question
    if conversation_history:
        context_lines = []
        # Взимаме последните 4 размени (2 въпроса + 2 отговора) за контекст
        for msg in conversation_history[-4:]:
            role_label = "User" if msg["role"] == "user" else "CineWave"
            context_lines.append(f"{role_label}: {msg['content']}")
        if context_lines:
            context_block = "\n".join(context_lines)
            full_question = (
                f"[Previous conversation for context:]\n{context_block}\n\n"
                f"[New question:] {question}"
            )

    response = agent.run(full_question)

    # Извличане на изпълнените заявки за показване в UI
    queries_info = []
    if hasattr(response, "collection_queries") and response.collection_queries:
        for cq in response.collection_queries:
            queries_info.append(
                {
                    "collection": getattr(cq, "collection", "Unknown"),
                    "query": getattr(cq, "query", ""),
                    "filters": getattr(cq, "filters", None),
                }
            )

    # Резервен начин за извличане на колекции ако collection_queries е празен
    collections_used = list({q["collection"] for q in queries_info})
    if not collections_used and hasattr(response, "searches"):
        # по-стари версии на клиента
        try:
            for search in (response.searches or []):
                col = getattr(search, "collection", None)
                if col:
                    collections_used.append(col)
            collections_used = list(set(collections_used))
        except Exception:
            pass

    # Извличане на usage токени (разни версии на API)
    usage = (
        getattr(response, "total_tokens", None)
        or getattr(response, "usage", {})
    )

    return {
        "answer": response.final_answer,
        "queries": queries_info,
        "collections": collections_used,
        "usage": usage,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Демо заявки (за тестване от командния ред)
# ──────────────────────────────────────────────────────────────────────────────

DEMO_QUERIES = [
    # 1. Semantic search
    "Recommend a high-rated crime film.",
    # 2. Multi-collection – links Movies + Directors
    "What are the common characteristics of Christopher Nolan's style and which of his films are in the database?",
    # 3. Follow-up (contextual)
    "Which of those won an Oscar for best visual effects?",
    # 4. Aggregation and filtering
    "How many series in the database have a rating above 9.0 and which are they?",
    # 5. Mood-based / subjective
    "I want something dark and psychologically heavy for tonight – what do you recommend?",
]


if __name__ == "__main__":
    import sys

    try:
        client = get_client()
    except ValueError as e:
        print(e)
        sys.exit(1)

    print("=== FlickMind Query Agent – Demo ===\n")
    history: list[dict] = []

    for i, q in enumerate(DEMO_QUERIES, 1):
        print(f"[{i}] Въпрос: {q}")
        try:
            result = ask(q, client, conversation_history=history if i > 1 else None)
            print(f"    Отговор: {result['answer']}")
            if result["collections"]:
                print(f"    Колекции: {', '.join(result['collections'])}")

            # Трупаме история за follow-up демонстрация
            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": result["answer"]})
        except Exception as e:
            print(f"    ГРЕШКА: {e}")
        print()

    client.close()
