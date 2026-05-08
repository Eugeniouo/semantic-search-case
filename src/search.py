import numpy as np
from sentence_transformers import util

def find_top3(query_text: str, model, corpus_embeddings: np.ndarray, corpus: list, top_k: int = 3) -> list:
    """
    находит top_k наиболее похожих фрагментов для текстового запроса
    возвращает список словарей с полями: id, score, function_name, description, rank
    """
    query_emb = model.encode(query_text, normalize_embeddings=True)

    # util.cos_sim может вернуть torch.Tensor, сразу конвертируем в numpy
    scores = util.cos_sim(query_emb, corpus_embeddings)[0]
    if hasattr(scores, 'cpu'):
        scores = scores.cpu().numpy()
        
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for rank, idx in enumerate(top_indices, start=1):
        results.append({
            "id": corpus[idx]["id"],    #chunk_id -> id
            "score": scores[idx],
            "function_name": corpus[idx]["function_name"],
            "description": corpus[idx]["description"],
            "rank": rank
        })
    return results

def search_all_questions(model, corpus_embeddings: np.ndarray, corpus: list, questions: list, top_k: int = 3) -> list:
    """
    выполняет поиск top_k для всех вопросов из списка
    возвращает список списков результатов (один подсписок на каждый вопрос)
    """
    return [find_top3(q["query"], model, corpus_embeddings, corpus, top_k) for q in questions]