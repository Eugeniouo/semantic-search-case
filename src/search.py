"""Семантический поиск по корпусу кода на основе косинусного сходства."""

import numpy as np
from sentence_transformers import util
from src.config import TOP_K

def find_top_k(
    query_text: str,
    model,
    corpus: list[dict],
    corpus_embeddings: np.ndarray,
    top_k: int = TOP_K,
) -> list[dict]:
    """
    Ищет top_k наиболее релевантных фрагментов кода для одного запроса.

    Args:
        query_text (str): Текст запроса (вопроса).
        model: Модель SentenceTransformer для векторизации.
        corpus (list[dict]): Исходный корпус кода.
        corpus_embeddings (np.ndarray): Предварительно вычисленная матрица эмбеддингов корпуса.
        top_k (int): Количество возвращаемых результатов. По умолчанию TOP_K.

    Returns:
        list[dict]: Список из top_k словарей с результатами поиска. Каждый словарь 
        содержит ключи: id, rank, score, function_name, category, description.
    """
    query_emb = model.encode(query_text, normalize_embeddings=True)

    scores = util.cos_sim(query_emb, corpus_embeddings)[0]
    if hasattr(scores, "cpu"):
        scores = scores.cpu().numpy()

    top_indices = np.argsort(scores)[::-1][:top_k]

    return [
        {
            "rank": rank,
            "id": corpus[idx]["id"],
            "score": float(scores[idx]),
            "function_name": corpus[idx]["function_name"],
            "category": corpus[idx]["category"],
            "description": corpus[idx]["description"],
        }
        for rank, idx in enumerate(top_indices, start=1)
    ]


def search_all_questions(
    questions: list[dict],
    model,
    corpus: list[dict],
    corpus_embeddings: np.ndarray,
    top_k: int = TOP_K,
) -> list[dict]:
    """
    Выполняет семантический поиск для списка вопросов и формирует сводный результат.

    Args:
        questions (list[dict]): Список тестовых вопросов.
        model: Модель SentenceTransformer для векторизации.
        corpus (list[dict]): Исходный корпус кода.
        corpus_embeddings (np.ndarray): Эмбеддинги корпуса кода.
        top_k (int): Глубина поиска для каждого вопроса.

    Returns:
        list[dict]: Список результатов по одному элементу на каждый вопрос.
        Ключи: question_id, query, language, correct_chunk_id, results.
    """
    outputs = []
    for question in questions:
        results = find_top_k(
            query_text=question["query"],
            model=model,
            corpus=corpus,
            corpus_embeddings=corpus_embeddings,
            top_k=top_k,
        )
        outputs.append({
            "question_id": question["question_id"],
            "query": question["query"],
            "language": question["language"],
            "correct_chunk_id": question["correct_chunk_id"],
            "results": results,
        })
    return outputs