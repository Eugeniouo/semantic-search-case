import pandas as pd


def precision_at_k(correct_ids: List[str], retrieved_lists: List[List[str]], k: int) -> float:
    if not correct_ids:
        return 0.0
    
    hits = sum(
        1 for c_id, r_list in zip(correct_ids, retrieved_lists)
        if c_id in r_list[:k]
    )
    return hits / len(correct_ids)


def reciprocal_rank(correct_id: str, retrieved_list: List[str]) -> float:
    try:
        rank = retrieved_list.index(correct_id) + 1  
        return 1.0 / rank
    except ValueError:
        return 0.0


def mrr(correct_ids: List[str], retrieved_lists: List[List[str]]) -> float:
    if not correct_ids:
        return 0.0
    
    rr_scores = [
        reciprocal_rank(c_id, r_list)
        for c_id, r_list in zip(correct_ids, retrieved_lists)
    ]
    return sum(rr_scores) / len(rr_scores)


def evaluate(
    correct_ids: List[str], 
    retrieved_lists: List[List[str]], 
    k: int
) -> Dict[str, Any]:
    return {
        "precision_at_k": precision_at_k(correct_ids, retrieved_lists, k),
        "mrr": mrr(correct_ids, retrieved_lists),
        "num_queries": len(correct_ids)
    }


def build_detailed_table(
    queries: List[str],
    correct_ids: List[str],
    retrieved_lists: List[List[str]],
    k: int 
) -> pd.DataFrame:
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