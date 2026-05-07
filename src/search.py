import numpy as np
from sentence_transformers import util

def find_top3(query_text, model, corpus_embeddings, corpus, top_k=3):
    """
    находит top_k наиболее похожих фрагментов для текстового запроса.
    
    Args:
        query_text: строка с запросом
        model: загруженная модель SentenceTransformer
        corpus_embeddings: np.array или torch.Tensor с эмбеддингами корпуса
        corpus: список словарей с исходными данными
        top_k: количество возвращаемых результатов
        
    Returns:
        list[dict]: список словарей с полями chunk_id, score, function_name, description
    """
    query_embedding = model.encode(query_text, normalize_embeddings=True)
    
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    
    top_indices = np.argsort(cos_scores.cpu().numpy())[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "chunk_id": corpus[idx]["id"],
            "score": cos_scores[idx].item(),
            "function_name": corpus[idx]["function_name"],
            "description": corpus[idx]["description"]
        })
        
    return results