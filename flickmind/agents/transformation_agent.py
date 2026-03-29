"""
FlickMind – Transformation Agent
=================================
Enriches collection objects by adding new AI-generated properties:
  • Movies   → ai_summary : short editorial summary
  • TVSeries → ai_tags    : auto-generated thematic tags (comma-separated)

WARNING: Transformation Agent modifies data in-place.
         Use only on test collections!

Changes vs original:
- iterator() doesn't accept limit — uses enumerate() instead
- Operations passed as TransformationOperation objects where required
- More robust wait_for_workflow with better logging
- get_transformed_samples is resilient against missing properties
"""

import os
import time
import weaviate
from weaviate.agents.transform import TransformationAgent
from weaviate.classes.config import Property, DataType
from dotenv import load_dotenv

load_dotenv()


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


def ensure_property_exists(
    client: weaviate.WeaviateClient,
    collection_name: str,
    prop_name: str,
    description: str,
) -> None:
    """Добавя ново свойство към колекцията ако вече не съществува."""
    collection = client.collections.get(collection_name)
    config = collection.config.get()
    existing = [p.name for p in config.properties]
    if prop_name not in existing:
        collection.config.add_property(
            Property(
                name=prop_name,
                data_type=DataType.TEXT,
                description=description,
            )
        )
        print(f"  Добавено свойство '{prop_name}' към {collection_name}")
    else:
        print(f"  Свойство '{prop_name}' вече съществува в {collection_name}")


def add_ai_summary_to_movies(client: weaviate.WeaviateClient) -> str:
    """
    Добавя 'ai_summary' към всеки филм в Movies.
    Връща workflow_id за проследяване на статуса.
    """
    ensure_property_exists(
        client,
        "Movies",
        "ai_summary",
        "AI-генерирано кратко резюме на филма (2-3 изречения)",
    )

    operations = [
        {
            "instruction": (
                "Write a concise 2-3 sentence summary of this movie that captures "
                "its essence, tone, and why it is significant in cinema history. "
                "Use the plot, genre, director, and awards fields as context. "
                "Write in a compelling, engaging style."
            ),
            "property": "ai_summary",
        }
    ]

    agent = TransformationAgent(
        client=client,
        collection="Movies",
        operations=operations,
    )

    response = agent.run()
    workflow_id = response.workflow_id
    print(f"  Transformation Agent стартиран. Workflow ID: {workflow_id}")
    return workflow_id


def add_ai_tags_to_series(client: weaviate.WeaviateClient) -> str:
    """
    Добавя 'ai_tags' към всеки сериал в TVSeries.
    Връща workflow_id за проследяване на статуса.
    """
    ensure_property_exists(
        client,
        "TVSeries",
        "ai_tags",
        "AI-генерирани тематични тагове (разделени със запетая)",
    )

    operations = [
        {
            "instruction": (
                "Generate 5-8 concise thematic tags for this TV series based on its "
                "plot, genre, and overall tone. Examples of good tags: "
                "'slow-burn', 'morally-complex', 'binge-worthy', 'critically-acclaimed', "
                "'based-on-true-events', 'ensemble-cast', 'mind-bending'. "
                "Return the tags as a comma-separated list, no quotes, no extra text."
            ),
            "property": "ai_tags",
        }
    ]

    agent = TransformationAgent(
        client=client,
        collection="TVSeries",
        operations=operations,
    )

    response = agent.run()
    workflow_id = response.workflow_id
    print(f"  Transformation Agent стартиран. Workflow ID: {workflow_id}")
    return workflow_id


def wait_for_workflow(
    client: weaviate.WeaviateClient,
    collection_name: str,
    workflow_id: str,
    timeout_sec: int = 180,
    poll_interval: int = 10,
) -> str:
    """
    Изчаква завършването на трансформацията.
    Връща крайния статус: 'completed', 'failed', 'timeout'.
    """
    # Нужен е agent instance само за get_workflow_status
    agent = TransformationAgent(client=client, collection=collection_name, operations=[])
    start = time.time()

    while time.time() - start < timeout_sec:
        try:
            status_resp = agent.get_workflow_status(workflow_id)
            status = status_resp.status.lower()
        except Exception as e:
            print(f"  Грешка при проверка на статус: {e}. Повторен опит...")
            time.sleep(poll_interval)
            continue

        if status in ("completed", "failed"):
            return status

        elapsed = int(time.time() - start)
        remaining = timeout_sec - elapsed
        print(f"  [{elapsed}s / {timeout_sec}s] Статус: {status} – изчакване ({remaining}s остават)...")
        time.sleep(poll_interval)

    return "timeout"


def get_transformed_samples(
    client: weaviate.WeaviateClient,
    collection_name: str,
    prop_name: str,
    limit: int = 3,
) -> list[dict]:
    """
    Връща примерни обекти с новото AI свойство.
    Използва enumerate() вместо limit параметър на iterator()
    (iterator() не приема limit в текущата версия на клиента).
    """
    collection = client.collections.get(collection_name)
    results = []

    try:
        for i, obj in enumerate(collection.iterator(return_properties=["title", prop_name])):
            if i >= limit * 3:  # Разглеждаме до 3x повече обекти в случай на липсващи стойности
                break
            props = obj.properties
            value = props.get(prop_name, "")
            if value:
                results.append(
                    {
                        "title": props.get("title", "—"),
                        prop_name: value,
                    }
                )
            if len(results) >= limit:
                break
    except Exception as e:
        print(f"  Предупреждение при извличане на примери: {e}")

    return results


# ──────────────────────────────────────────────────────────────────────────────
# CLI demo
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    try:
        client = get_client()
    except ValueError as e:
        print(e)
        sys.exit(1)

    print("=== FlickMind Transformation Agent ===\n")

    print("Стартиране на трансформация за Movies (ai_summary)...")
    wf_movies = add_ai_summary_to_movies(client)

    print("\nСтартиране на трансформация за TVSeries (ai_tags)...")
    wf_series = add_ai_tags_to_series(client)

    print("\nИзчакване на Movies трансформация...")
    status_m = wait_for_workflow(client, "Movies", wf_movies)
    print(f"  Краен статус Movies: {status_m}")

    print("\nИзчакване на TVSeries трансформация...")
    status_s = wait_for_workflow(client, "TVSeries", wf_series)
    print(f"  Краен статус TVSeries: {status_s}")

    if status_m == "completed":
        print("\nПримерни ai_summary от Movies:")
        for s in get_transformed_samples(client, "Movies", "ai_summary"):
            preview = s["ai_summary"][:120]
            print(f"  📽  {s['title']}: {preview}...")
    else:
        print(f"\nMovies трансформация завърши със статус: {status_m}")

    if status_s == "completed":
        print("\nПримерни ai_tags от TVSeries:")
        for s in get_transformed_samples(client, "TVSeries", "ai_tags"):
            print(f"  📺  {s['title']}: {s['ai_tags']}")
    else:
        print(f"\nTVSeries трансформация завърши със статус: {status_s}")

    client.close()
    print("\nГотово!")
