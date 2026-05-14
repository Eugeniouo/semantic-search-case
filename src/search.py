"""Семантический поиск по корпусу кода на основе косинусного сходства"""

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
    Ищет top_k наиболее похожих фрагментов для одного текстового запроса.

    Возвращает список словарей с полями:
    id, rank, score, function_name, category, description.
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
    Прогоняет все вопросы через поиск и возвращает результаты в едином формате.

    Возвращает список словарей, один элемент на вопрос:
    question_id, query, language, correct_chunk_id, results.
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