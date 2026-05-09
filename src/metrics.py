"""
Модуль подсчёта метрик качества информационного поиска.

Реализует стандартные метрики ранжирования: Precision@K и MRR,
утилиты для построения сводной таблицы результатов поиска.
"""

import pandas as pd

def precision_at_k(correct_ids: list[str], retrieved_lists: list[list[str]], k: int) -> float:
    """
    Вычисляет Precision@K - доля запросов, для которых правильный
    ответ оказался в первых k результатах.

    Args:
        correct_ids: список правильных идентификаторов, по одному на запрос.
        retrieved_lists: список списков найденных идентификаторов в порядке ранга.
        k: глубина среза.

    Returns:
        Значение метрики в диапазоне [0.0, 1.0].
    """
    if not correct_ids:
        return 0.0
    
    hits = sum(
        1 for c_id, r_list in zip(correct_ids, retrieved_lists)
        if c_id in r_list[:k]
    )

    return hits / len(correct_ids)


def reciprocal_rank(correct_id: str, retrieved_list: list[str]) -> float:
    """
    Вычисляет Reciprocal Rank для одного запроса, величинf 1/rank,
    где rank это позиция правильного ответа в списке результатов.

    Args:
        correct_id: правильный идентификатор для данного запроса.
        retrieved_list: список найденных идентификаторов в порядке ранга.

    Returns:
        1/rank если correct_id найден, иначе 0.0.
    """
    try:
        rank = retrieved_list.index(correct_id) + 1  
        return 1.0 / rank
    except ValueError:
        return 0.0


def mrr(correct_ids: list[str], retrieved_lists: list[list[str]]) -> float:
    """
    Вычисляет MRR. Среднее значение Reciprocal Rank
    по всем запросам.

    Args:
        correct_ids: список правильных идентификаторов по одному на запрос.
        retrieved_lists: список списков найденных идентификаторов в порядке ранга

    Returns:
        Значение MRR в диапазоне [0.0, 1.0]
    """
    if not correct_ids:
        return 0.0
    
    rr_scores = [
        reciprocal_rank(c_id, r_list)
        for c_id, r_list in zip(correct_ids, retrieved_lists)
    ]
    return sum(rr_scores) / len(rr_scores)


def evaluate(
    correct_ids: list[str], 
    retrieved_lists: list[list[str]], 
    k: int
) -> dict[str, int | float]:
    """
    Вычисляет сводные метрики качества поиска.

    Args:
        correct_ids: список правильных идентификаторов, по одному на запрос.
        retrieved_lists: список списков найденных идентификаторов в порядке ранга
        k: глубина среза для Precision@K.

    Returns:
        Словарь с ключами precision_at_{k}, mrr и num_queries
    """
    return {
        f"precision_at_{k}": precision_at_k(correct_ids, retrieved_lists, k),
        "mrr": mrr(correct_ids, retrieved_lists),
        "num_queries": len(correct_ids)
    }


def build_detailed_table(
    queries: list[str],
    correct_ids: list[str],
    retrieved_lists: list[list[str]],
    k: int 
) -> pd.DataFrame:
    """
    Строит детальную таблицу результатов поиска по каждому запросу.

    Args:
        queries: список текстов запросов
        correct_ids: список правильных идентификаторов, по одному на запрос.
        retrieved_lists: список списков найденных идентификаторов в порядке ранга.
        k: глубина среза для определения hit.

    Returns:
        DataFrame с колонками: query, correct_id, retrieved_ids, rank, hit.
        rank равен None если правильный ответ не найден,
        hit равен True если rank <= k.
    """
    rows = []
    for q, c_id, r_list in zip(queries, correct_ids, retrieved_lists):
        try:
            rank = r_list.index(c_id) + 1
            hit = rank <= k
        except ValueError:
            rank = None
            hit = False
            
        rows.append({
            "query": q,
            "correct_id": c_id,
            "retrieved_ids": r_list,
            "rank": rank,
            "hit": hit
        })
        
    return pd.DataFrame(rows)