"""Загрузка файлов датасета."""

import json
from pathlib import Path

from src.config import QUESTIONS_PATH, CATEGORIES_PATH, CORPUS_PATH

def load_corpus(path: Path = CORPUS_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_questions(path: Path = QUESTIONS_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)
    
def load_categories(path: Path = CATEGORIES_PATH) -> dict[str, dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return {item["key"]: item for item in data["categories"]}

def load_dataset() -> tuple[list[dict], list[dict], dict[str, dict]]:
    """
    Загружает все три датасета одним вызовом.

    Returns:
        tuple: Кортеж из трех элементов:
            - corpus (list[dict]): Корпус фрагментов кода.
            - questions (list[dict]): Набор тестовых вопросов.
            - categories (dict[str, dict]): Словарь категорий (где ключ - идентификатор категории).
    """
    corpus = load_corpus()
    questions = load_questions()
    categories = load_categories()

    return corpus, questions, categories