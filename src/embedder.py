from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

"""
Модуль для преобразования корпуса кода в эмбеддинги.

Содержит функции для:
- преобразования записи корпуса в текст
- получения эмбеддингов через sentence-transformers
- сохранения и загрузки эмбеддингов из кеша (.npy)
- работы с кешированием по имени модели
"""


def record_to_text(record: dict) -> str:
    """
    Преобразует одну запись корпуса в текст для модели.

    Args:
        record (dict): запись корпуса с полями:
            function_name, language, description, code

    Returns:
        str: текстовое представление записи
    """
    return f"""
Function: {record.get('function_name', '')}
Language: {record.get('language', '')}
Description: {record.get('description', '')}
Code:
{record.get('code', '')}
""".strip()



# генерация эмбеддингов
def get_embeddings(texts: list[str], model_name: str) -> np.ndarray:
    # загружает модель и считает эмбеддинги для списка текстов.
    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    return embeddings

# сохранение эмбеддингов
def save_embeddings(path: str, embeddings: np.ndarray) -> None:
    # cохраняет эмбеддинги в .npy файл.
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    np.save(path, embeddings)


# загрузка эмбеддингов
def load_embeddings(path: str) -> np.ndarray:
    #загружает эмбеддинги из .npy файла.
    return np.load(path)


# путь до кэша
def get_cache_path(model_name: str) -> str:
    # возвращает путь до файла с кэшем эмбеддингов для модели.
    safe_name = model_name.replace("/", "_")
    return f"cache/{safe_name}.npy"


# функция получения эмбеддинга (с кэшем)
def get_or_compute_embeddings(texts: list[str], model_name: str) -> np.ndarray:
    # если ембеддинги уже считались - загружает их, иначе считает
    path = get_cache_path(model_name)

    if Path(path).exists():
        print("Loading embedding from the cache...")
        return load_embeddings(path)

    print("Count the embeddings...")
    embeddings = get_embeddings(texts, model_name)
    save_embeddings(path, embeddings)

    print("Saved to the cache: ", path)
    return embeddings