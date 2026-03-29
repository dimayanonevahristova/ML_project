

import os
import sys
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from dotenv import load_dotenv

load_dotenv()

MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": "Drama",
        "director": "Frank Darabont",
        "rating": 9.3,
        "plot": (
            "Two imprisoned men bond over a number of years, finding solace and "
            "eventual redemption through acts of common decency."
        ),
        "duration_min": 142,
        "language": "English",
        "country": "USA",
        "awards": "Nominated for 7 Academy Awards",
    },
    {
        "title": "The Godfather",
        "year": 1972,
        "genre": "Crime, Drama",
        "director": "Francis Ford Coppola",
        "rating": 9.2,
        "plot": (
            "The aging patriarch of an organized crime dynasty transfers control "
            "of his clandestine empire to his reluctant son."
        ),
        "duration_min": 175,
        "language": "English",
        "country": "USA",
        "awards": "Won 3 Academy Awards including Best Picture",
    },
    {
        "title": "Schindler's List",
        "year": 1993,
        "genre": "Biography, Drama, History",
        "director": "Steven Spielberg",
        "rating": 9.0,
        "plot": (
            "In German-occupied Poland during World War II, industrialist Oskar "
            "Schindler gradually becomes concerned for his Jewish workforce after "
            "witnessing their persecution by the Nazis."
        ),
        "duration_min": 195,
        "language": "English, Hebrew, German, Polish",
        "country": "USA",
        "awards": "Won 7 Academy Awards including Best Picture",
    },
    {
        "title": "Pulp Fiction",
        "year": 1994,
        "genre": "Crime, Drama",
        "director": "Quentin Tarantino",
        "rating": 8.9,
        "plot": (
            "The lives of two mob hitmen, a boxer, a gangster and his wife, and a "
            "pair of diner bandits intertwine in four tales of violence and redemption."
        ),
        "duration_min": 154,
        "language": "English",
        "country": "USA",
        "awards": "Won Palme d'Or at Cannes, Nominated for 7 Academy Awards",
    },
    {
        "title": "Inception",
        "year": 2010,
        "genre": "Action, Adventure, Sci-Fi",
        "director": "Christopher Nolan",
        "rating": 8.8,
        "plot": (
            "A thief who steals corporate secrets through the use of dream-sharing "
            "technology is given the inverse task of planting an idea into the mind of a C.E.O."
        ),
        "duration_min": 148,
        "language": "English, Japanese, French",
        "country": "USA, UK",
        "awards": "Won 4 Academy Awards",
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action, Crime, Drama",
        "director": "Christopher Nolan",
        "rating": 9.0,
        "plot": (
            "When the menace known as the Joker wreaks havoc and chaos on the people "
            "of Gotham, Batman must accept one of the greatest psychological and "
            "physical tests of his ability to fight injustice."
        ),
        "duration_min": 152,
        "language": "English",
        "country": "USA, UK",
        "awards": "Won 2 Academy Awards",
    },
    {
        "title": "Parasite",
        "year": 2019,
        "genre": "Comedy, Drama, Thriller",
        "director": "Bong Joon-ho",
        "rating": 8.5,
        "plot": (
            "Greed and class discrimination threaten the newly formed symbiotic "
            "relationship between the wealthy Park family and the destitute Kim clan."
        ),
        "duration_min": 132,
        "language": "Korean",
        "country": "South Korea",
        "awards": "Won 4 Academy Awards including Best Picture",
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "genre": "Adventure, Drama, Sci-Fi",
        "director": "Christopher Nolan",
        "rating": 8.7,
        "plot": (
            "A team of explorers travel through a wormhole in space in an attempt "
            "to ensure humanity's survival."
        ),
        "duration_min": 169,
        "language": "English",
        "country": "USA, UK, Canada",
        "awards": "Won Academy Award for Best Visual Effects",
    },
    {
        "title": "The Matrix",
        "year": 1999,
        "genre": "Action, Sci-Fi",
        "director": "Lana Wachowski, Lilly Wachowski",
        "rating": 8.7,
        "plot": (
            "A computer hacker learns from mysterious rebels about the true nature "
            "of his reality and his role in the war against its controllers."
        ),
        "duration_min": 136,
        "language": "English",
        "country": "USA, Australia",
        "awards": "Won 4 Academy Awards",
    },
    {
        "title": "Spirited Away",
        "year": 2001,
        "genre": "Animation, Adventure, Family",
        "director": "Hayao Miyazaki",
        "rating": 8.6,
        "plot": (
            "During her family's move to the suburbs, a sulky 10-year-old girl wanders "
            "into a world ruled by gods, witches, and spirits, where humans are changed into beasts."
        ),
        "duration_min": 125,
        "language": "Japanese",
        "country": "Japan",
        "awards": "Won Academy Award for Best Animated Feature",
    },
    {
        "title": "12 Angry Men",
        "year": 1957,
        "genre": "Crime, Drama",
        "director": "Sidney Lumet",
        "rating": 9.0,
        "plot": (
            "The jury in a New York City murder trial is frustrated by a single "
            "member whose skeptical caution forces them to reconsider the case."
        ),
        "duration_min": 96,
        "language": "English",
        "country": "USA",
        "awards": "Nominated for 3 Academy Awards, Won 3 BAFTAs",
    },
    {
        "title": "Oldboy",
        "year": 2003,
        "genre": "Action, Drama, Mystery",
        "director": "Park Chan-wook",
        "rating": 8.4,
        "plot": (
            "After being imprisoned in a makeshift cell for 15 years without "
            "explanation, a man is released and given five days to find his captor."
        ),
        "duration_min": 120,
        "language": "Korean",
        "country": "South Korea",
        "awards": "Won Grand Prix at Cannes Film Festival",
    },
]

TV_SERIES = [
    {
        "title": "Breaking Bad",
        "start_year": 2008,
        "end_year": 2013,
        "genre": "Crime, Drama, Thriller",
        "creator": "Vince Gilligan",
        "rating": 9.5,
        "plot": (
            "A chemistry teacher diagnosed with inoperable lung cancer turns to "
            "manufacturing and selling methamphetamine with a former student in "
            "order to secure his family's future."
        ),
        "seasons": 5,
        "episodes": 62,
        "network": "AMC",
        "status": "Ended",
        "country": "USA",
    },
    {
        "title": "Game of Thrones",
        "start_year": 2011,
        "end_year": 2019,
        "genre": "Action, Adventure, Drama",
        "creator": "David Benioff, D.B. Weiss",
        "rating": 9.2,
        "plot": (
            "Nine noble families fight for control over the lands of Westeros, "
            "while an ancient enemy returns after being dormant for millennia."
        ),
        "seasons": 8,
        "episodes": 73,
        "network": "HBO",
        "status": "Ended",
        "country": "USA, UK",
    },
    {
        "title": "Chernobyl",
        "start_year": 2019,
        "end_year": 2019,
        "genre": "Drama, History, Thriller",
        "creator": "Craig Mazin",
        "rating": 9.4,
        "plot": (
            "In April 1986, an explosion at the Chernobyl nuclear power plant in "
            "the USSR becomes one of the world's worst nuclear disasters."
        ),
        "seasons": 1,
        "episodes": 5,
        "network": "HBO",
        "status": "Ended",
        "country": "USA, UK",
    },
    {
        "title": "The Wire",
        "start_year": 2002,
        "end_year": 2008,
        "genre": "Crime, Drama, Thriller",
        "creator": "David Simon",
        "rating": 9.3,
        "plot": (
            "The Baltimore drug scene, as seen through the eyes of drug dealers "
            "and law enforcement."
        ),
        "seasons": 5,
        "episodes": 60,
        "network": "HBO",
        "status": "Ended",
        "country": "USA",
    },
    {
        "title": "Stranger Things",
        "start_year": 2016,
        "end_year": 2025,
        "genre": "Drama, Fantasy, Horror",
        "creator": "Matt Duffer, Ross Duffer",
        "rating": 8.7,
        "plot": (
            "When a young boy disappears, his mother, a police chief and his friends "
            "must confront terrifying supernatural forces in order to get him back."
        ),
        "seasons": 5,
        "episodes": 42,
        "network": "Netflix",
        "status": "Ended",
        "country": "USA",
    },
    {
        "title": "Dark",
        "start_year": 2017,
        "end_year": 2020,
        "genre": "Crime, Drama, Mystery",
        "creator": "Baran bo Odar, Jantje Friese",
        "rating": 8.8,
        "plot": (
            "A family saga with a supernatural twist, set in a German town where "
            "the disappearance of two young children exposes the relationships "
            "among four families."
        ),
        "seasons": 3,
        "episodes": 26,
        "network": "Netflix",
        "status": "Ended",
        "country": "Germany",
    },
    {
        "title": "Succession",
        "start_year": 2018,
        "end_year": 2023,
        "genre": "Drama",
        "creator": "Jesse Armstrong",
        "rating": 8.9,
        "plot": (
            "The Roy family is known for controlling the biggest media and "
            "entertainment company in the world. Their world changes when their "
            "father steps down from the company."
        ),
        "seasons": 4,
        "episodes": 39,
        "network": "HBO",
        "status": "Ended",
        "country": "USA",
    },
    {
        "title": "The Last of Us",
        "start_year": 2023,
        "end_year": 0,
        "genre": "Action, Adventure, Drama",
        "creator": "Craig Mazin, Neil Druckmann",
        "rating": 8.8,
        "plot": (
            "After a global catastrophe, a hardened survivor takes charge of a "
            "14-year-old girl who may be humanity's last hope."
        ),
        "seasons": 2,
        "episodes": 16,
        "network": "HBO",
        "status": "Ongoing",
        "country": "USA",
    },
    {
        "title": "Better Call Saul",
        "start_year": 2015,
        "end_year": 2022,
        "genre": "Crime, Drama",
        "creator": "Vince Gilligan, Peter Gould",
        "rating": 9.0,
        "plot": (
            "The trials and tribulations of criminal lawyer Jimmy McGill in the "
            "time before he established his Saul Goodman persona."
        ),
        "seasons": 6,
        "episodes": 63,
        "network": "AMC",
        "status": "Ended",
        "country": "USA",
    },
    {
        "title": "Severance",
        "start_year": 2022,
        "end_year": 0,
        "genre": "Drama, Mystery, Sci-Fi",
        "creator": "Dan Erickson",
        "rating": 8.7,
        "plot": (
            "Mark leads a team of office workers whose memories have been surgically "
            "divided between their work and personal lives."
        ),
        "seasons": 2,
        "episodes": 19,
        "network": "Apple TV+",
        "status": "Ongoing",
        "country": "USA",
    },
]

DIRECTORS = [
    {
        "name": "Christopher Nolan",
        "birth_year": 1970,
        "nationality": "British-American",
        "style": "Complex narratives, practical effects, non-linear storytelling, temporal manipulation",
        "biography": (
            "Christopher Nolan is a British-American filmmaker known for his distinctive "
            "storytelling style, often featuring non-linear narratives and practical effects. "
            "His films have grossed over $5 billion worldwide. He frequently collaborates "
            "with composer Hans Zimmer and cinematographer Hoyte van Hoytema."
        ),
        "notable_works": "The Dark Knight Trilogy, Inception, Interstellar, Dunkirk, Oppenheimer",
        "awards": "Academy Award for Best Director for Oppenheimer 2024",
        "active_since": 1998,
    },
    {
        "name": "Quentin Tarantino",
        "birth_year": 1963,
        "nationality": "American",
        "style": "Nonlinear stories, stylized violence, pop culture references, sharp dialogue",
        "biography": (
            "Quentin Tarantino is an American filmmaker, actor, and author. His films are "
            "characterized by nonlinear storylines, aestheticization of violence, extended "
            "dialogue, ensemble casts, and references to popular culture. He started as a "
            "video store clerk and is largely self-taught."
        ),
        "notable_works": "Pulp Fiction, Kill Bill, Inglourious Basterds, Django Unchained, The Hateful Eight",
        "awards": "2 Academy Awards for Best Original Screenplay",
        "active_since": 1992,
    },
    {
        "name": "Steven Spielberg",
        "birth_year": 1946,
        "nationality": "American",
        "style": "Emotional storytelling, crowd-pleasing blockbusters, historical dramas",
        "biography": (
            "Steven Spielberg is one of the most influential filmmakers in cinema history. "
            "He pioneered the modern blockbuster with Jaws and has since directed some of "
            "the highest-grossing and most acclaimed films ever made. His work spans genres "
            "from adventure to historical drama."
        ),
        "notable_works": "Schindler's List, Jaws, E.T., Raiders of the Lost Ark, Saving Private Ryan",
        "awards": "3 Academy Awards including 2 for Best Director",
        "active_since": 1971,
    },
    {
        "name": "Bong Joon-ho",
        "birth_year": 1969,
        "nationality": "South Korean",
        "style": "Genre-blending, social commentary, dark comedy, unexpected tonal shifts",
        "biography": (
            "Bong Joon-ho is a South Korean filmmaker whose works explore themes of class "
            "conflict, social inequality, and the human condition. His 2019 film Parasite "
            "became the first non-English language film to win the Academy Award for Best Picture."
        ),
        "notable_works": "Parasite, Memories of Murder, The Host, Snowpiercer, Okja",
        "awards": "4 Academy Awards for Parasite including Best Picture and Best Director",
        "active_since": 2000,
    },
    {
        "name": "Hayao Miyazaki",
        "birth_year": 1941,
        "nationality": "Japanese",
        "style": "Hand-drawn animation, environmentalism, coming-of-age, Japanese folklore",
        "biography": (
            "Hayao Miyazaki is a Japanese animator, filmmaker, and manga artist and a "
            "co-founder of Studio Ghibli. His works are characterized by their detailed "
            "animation, complex female protagonists, and themes of pacifism, environmentalism, "
            "and the power of the natural world."
        ),
        "notable_works": "Spirited Away, My Neighbor Totoro, Princess Mononoke, Howl's Moving Castle",
        "awards": "Academy Award for Best Animated Feature for Spirited Away, Honorary Oscar",
        "active_since": 1963,
    },
    {
        "name": "Francis Ford Coppola",
        "birth_year": 1939,
        "nationality": "American",
        "style": "Epic storytelling, operatic drama, intimate character study within grand scale",
        "biography": (
            "Francis Ford Coppola is an American film director, producer, and screenwriter "
            "who was a central figure in the New Hollywood movement. His Godfather trilogy "
            "is considered one of the greatest achievements in cinema history."
        ),
        "notable_works": "The Godfather, The Godfather Part II, Apocalypse Now, The Conversation",
        "awards": "5 Academy Awards including Best Director and Best Picture for The Godfather Part II",
        "active_since": 1962,
    },
]

def get_client() -> weaviate.WeaviateClient:
    # При зареждане OpenAI ключ не е нужен (vectorizer е text2vec_weaviate)
    # Нужен е само при Query Agent / Transformation Agent заявки
    required = ["WEAVIATE_URL", "WEAVIATE_API_KEY"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise ValueError(
            f"Липсващи environment variables: {', '.join(missing)}\n"
            "Копирайте .env.example → .env и попълнете ключовете."
        )

    return weaviate.connect_to_weaviate_cloud(
        cluster_url=os.environ["WEAVIATE_URL"],
        auth_credentials=weaviate.auth.AuthApiKey(os.environ["WEAVIATE_API_KEY"]),
        # Без X-OpenAI-Api-Key – vectorizer е text2vec_weaviate (вграден)
    )


def delete_collections_if_exist(client: weaviate.WeaviateClient) -> None:
    for name in ["Movies", "TVSeries", "Directors"]:
        if client.collections.exists(name):
            client.collections.delete(name)
            print(f"  Изтрита колекция: {name}")


def create_movies_collection(client: weaviate.WeaviateClient) -> None:
    client.collections.create(
        name="Movies",
        description="Колекция с информация за филми",
        vectorizer_config=Configure.Vectorizer.text2vec_weaviate(),
        generative_config=Configure.Generative.openai(),
        properties=[
            Property(name="title",        data_type=DataType.TEXT,   description="Заглавие"),
            Property(name="year",         data_type=DataType.INT,    description="Година"),
            Property(name="genre",        data_type=DataType.TEXT,   description="Жанр"),
            Property(name="director",     data_type=DataType.TEXT,   description="Режисьор"),
            Property(name="rating",       data_type=DataType.NUMBER, description="IMDb рейтинг"),
            Property(name="plot",         data_type=DataType.TEXT,   description="Сюжет"),
            Property(name="duration_min", data_type=DataType.INT,    description="Продължителност (мин)"),
            Property(name="language",     data_type=DataType.TEXT,   description="Език"),
            Property(name="country",      data_type=DataType.TEXT,   description="Страна"),
            Property(name="awards",       data_type=DataType.TEXT,   description="Награди"),
        ],
    )
    print("  Създадена колекция: Movies")


def create_tvseries_collection(client: weaviate.WeaviateClient) -> None:
    client.collections.create(
        name="TVSeries",
        description="Колекция с информация за сериали",
        vectorizer_config=Configure.Vectorizer.text2vec_weaviate(),
        generative_config=Configure.Generative.openai(),
        properties=[
            Property(name="title",      data_type=DataType.TEXT,   description="Заглавие"),
            Property(name="start_year", data_type=DataType.INT,    description="Начална година"),
            Property(name="end_year",   data_type=DataType.INT,    description="Крайна година (0=продължава)"),
            Property(name="genre",      data_type=DataType.TEXT,   description="Жанр"),
            Property(name="creator",    data_type=DataType.TEXT,   description="Създател"),
            Property(name="rating",     data_type=DataType.NUMBER, description="IMDb рейтинг"),
            Property(name="plot",       data_type=DataType.TEXT,   description="Сюжет"),
            Property(name="seasons",    data_type=DataType.INT,    description="Сезони"),
            Property(name="episodes",   data_type=DataType.INT,    description="Епизоди"),
            Property(name="network",    data_type=DataType.TEXT,   description="Платформа"),
            Property(name="status",     data_type=DataType.TEXT,   description="Статус"),
            Property(name="country",    data_type=DataType.TEXT,   description="Страна"),
        ],
    )
    print("  Създадена колекция: TVSeries")


def create_directors_collection(client: weaviate.WeaviateClient) -> None:
    client.collections.create(
        name="Directors",
        description="Колекция с информация за режисьори",
        vectorizer_config=Configure.Vectorizer.text2vec_weaviate(),
        generative_config=Configure.Generative.openai(),
        properties=[
            Property(name="name",          data_type=DataType.TEXT, description="Пълно име"),
            Property(name="birth_year",    data_type=DataType.INT,  description="Година на раждане"),
            Property(name="nationality",   data_type=DataType.TEXT, description="Националност"),
            Property(name="style",         data_type=DataType.TEXT, description="Режисьорски стил"),
            Property(name="biography",     data_type=DataType.TEXT, description="Биография"),
            Property(name="notable_works", data_type=DataType.TEXT, description="Известни творби"),
            Property(name="awards",        data_type=DataType.TEXT, description="Награди"),
            Property(name="active_since",  data_type=DataType.INT,  description="Активен от"),
        ],
    )
    print("  Създадена колекция: Directors")


def load_batch(collection, items: list, label: str) -> int:
    success_count = 0
    with collection.batch.dynamic() as batch:
        for item in items:
            batch.add_object(properties=item)

    # Проверка за грешки след batch
    if collection.batch.failed_objects:
        failed = len(collection.batch.failed_objects)
        print(f"  ⚠️  {failed} обекта не бяха заредени в {label}")
        success_count = len(items) - failed
    else:
        success_count = len(items)

    return success_count


def main():
    print("\nFlickMind – Loading data into Weaviate Cloud\n")

    try:
        client = get_client()
    except ValueError as e:
        print(e)
        sys.exit(1)

    try:
        meta = client.get_meta()
        print(f"Свързан към Weaviate. Версия: {meta['version']}\n")
    except Exception as e:
        print(f"Грешка при свързване: {e}")
        sys.exit(1)

    print("Изчистване на стари колекции...")
    delete_collections_if_exist(client)

    print("\nСъздаване на колекции...")
    create_movies_collection(client)
    create_tvseries_collection(client)
    create_directors_collection(client)

    print("\nЗареждане на данни...")

    movies_col = client.collections.get("Movies")
    n_movies = load_batch(movies_col, MOVIES, "Movies")
    print(f"  ✓ Заредени {n_movies}/{len(MOVIES)} филма")

    series_col = client.collections.get("TVSeries")
    n_series = load_batch(series_col, TV_SERIES, "TVSeries")
    print(f"  ✓ Заредени {n_series}/{len(TV_SERIES)} сериала")

    dirs_col = client.collections.get("Directors")
    n_dirs = load_batch(dirs_col, DIRECTORS, "Directors")
    print(f"  ✓ Заредени {n_dirs}/{len(DIRECTORS)} режисьора")

    total = n_movies + n_series + n_dirs
    expected = len(MOVIES) + len(TV_SERIES) + len(DIRECTORS)
    print(f"\nОбщо: {total}/{expected} обекта заредени успешно.")

    client.close()

    if total == expected:
        print("Всичко е заредено успешно! ✓\n")
    else:
        print("Зареждането завърши с предупреждения. Проверете изхода по-горе.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
