"""Модуль для преобразования корпуса кода в эмбеддинги."""

from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import OUTPUTS_DIR

def record_to_text(record: dict) -> str:
    """
    Преобразует одну запись корпуса в текст для подачи в модель.

    Args:
        record (dict): Запись корпуса с полями 'function_name', 'language', 'description', 'code'.

    Returns:
        str: Текстовое представление записи, готовое для векторизации.
    """
    return f"""
function: {record['function_name']}
language: {record['language']}
description: {record['description']}
code:
{record['code']}
""".strip()


def get_embeddings(texts: list[str], model_name: str) -> np.ndarray:
    """
    Вычисляет эмбеддинги для списка текстов.

    Args:
        texts (list[str]): список текстов
        model_name (str): имя модели sentence-transformers

    Returns:
        np.ndarray: матрица эмбеддингов
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings


def save_embeddings(path: str, embeddings: np.ndarray) -> None:
    """
    Сохраняет эмбеддинги в .npy файл.

    Args:
        path (str): путь к файлу
        embeddings (np.ndarray): матрица эмбеддингов
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    np.save(path, embeddings)



def load_embeddings(path: str) -> np.ndarray:
    """
    Загружает эмбеддинги из .npy файла.

    Args:
        path (str): путь к файлу

    Returns:
        np.ndarray: матрица эмбеддингов
    """
    return np.load(path)



def get_cache_path(model_name: str) -> str:
    """
    Возвращает путь к файлу кеша для модели.

    Args:
        model_name (str): имя модели

    Returns:
        str: путь к кешу
    """
    safe_name = model_name.replace("/", "_")
    return str(OUTPUTS_DIR / f"{safe_name}.npy")



def get_or_compute_embeddings(texts: list[str], model_name: str) -> np.ndarray:
    """
    Загружает эмбеддинги из кеша или вычисляет их заново.

    Args:
        texts (list[str]): список текстов
        model_name (str): имя модели

    Returns:
        np.ndarray: матрица эмбеддингов
    """
    path = get_cache_path(model_name)

    if Path(path).exists():
        print("loading embedding from the cache...")
        return load_embeddings(path)

    print("count the embeddings...")
    embeddings = get_embeddings(texts, model_name)
    save_embeddings(path, embeddings)

    print("saved to the cache: ", path)
    return embeddings
