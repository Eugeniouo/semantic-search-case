"""
Модуль подсчёта метрик качества информационного поиска.

Реализует стандартные метрики ранжирования: Precision@K и MRR,
утилиты для построения сводной таблицы результатов поиска.
"""

import pandas as pd
from src.config import TOP_K

def reciprocal_rank(results: list[dict], correct_id: str) -> float:
    """
    Вычисляет Reciprocal Rank для одного запроса.

    Args:
        results: список найденных фрагментов с полями id и rank.
        correct_id: правильный идентификатор для данного запроса.

    Returns:
        1/rank если correct_id найден, иначе 0.0.
    """
    for result in results:
        if result["id"] == correct_id:
            return 1.0 / result["rank"]
    return 0.0


def precision_at_k(search_outputs: list[dict], k: int = TOP_K) -> float:
    """
    Вычисляет Precision@K, доля запросов для которых правильный
    ответ оказался в первых k результатах.

    Args:
        search_outputs: результаты search_all_questions().
        k: глубина среза.

    Returns:
        Значение метрики в диапазоне [0.0, 1.0].
    """
    if not search_outputs:
        return 0.0

    hits = sum(
        1 for output in search_outputs
        if output["correct_chunk_id"] in
           [r["id"] for r in output["results"][:k]]
    )
    return hits / len(search_outputs)


def mrr(search_outputs: list[dict]) -> float:
    """
    Вычисляет MRR, среднее значение Reciprocal Rank по всем запросам.

    Args:
        search_outputs: результаты search_all_questions().

    Returns:
        Значение MRR в диапазоне [0.0, 1.0].
    """
    if not search_outputs:
        return 0.0

    rr_scores = [
        reciprocal_rank(output["results"], output["correct_chunk_id"])
        for output in search_outputs
    ]
    return sum(rr_scores) / len(rr_scores)


def evaluate(search_outputs: list[dict], k: int = TOP_K) -> dict[str, int | float]:
    """
    Вычисляет сводные метрики качества поиска.

    Args:
        search_outputs: результаты search_all_questions().
        k: глубина среза для Precision@K.

    Returns:
        Словарь с ключами precision_at_{k}, mrr и num_questions.
    """
    return {
        f"precision_at_{k}": precision_at_k(search_outputs, k),
        "mrr": mrr(search_outputs),
        "num_questions": len(search_outputs),
    }


def build_detailed_table(search_outputs: list[dict], k: int = TOP_K) -> pd.DataFrame:
    """
    Строит детальную таблицу результатов поиска по каждому запросу.
    Удобна для анализа ошибок, показывает что нашлось и на какой позиции.

    Args:
        search_outputs: результаты search_all_questions().
        k: глубина среза для определения hit.

    Returns:
        DataFrame с колонками: question_id, query, language,
        correct_chunk_id, top_1, top_2, top_3, rank, hit.
        rank равен None если правильный ответ не найден в выдаче.
    """
    rows = []
    for output in search_outputs:
        correct_id = output["correct_chunk_id"]
        ranked_ids = [r["id"] for r in output["results"]]

        try:
            rank = ranked_ids.index(correct_id) + 1
            hit = rank <= k
        except ValueError:
            rank = None
            hit = False

        rows.append({
            "question_id": output["question_id"],
            "query": output["query"],
            "language": output["language"],
            "correct_chunk_id": correct_id,
            "top_1": ranked_ids[0] if len(ranked_ids) > 0 else None,
            "top_2": ranked_ids[1] if len(ranked_ids) > 1 else None,
            "top_3": ranked_ids[2] if len(ranked_ids) > 2 else None,
            "rank": rank,
            "hit": hit,
        })

    return pd.DataFrame(rows)