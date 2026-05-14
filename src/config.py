"""Единый файл для подключения путей, модулей и гиперпараметров"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CORPUS_PATH = ROOT / "data" / "code_corpus.json"
QUESTIONS_PATH = ROOT / "data" / "eval_questions.json"
CATEGORIES_PATH = ROOT / "data" / "categories.json"

OUTPUTS_DIR = ROOT / "outputs"

MODELS = [
    "paraphrase-multilingual-MiniLM-L12-v2",
    "paraphrase-multilingual-mpnet-base-v2",
    "intfloat/multilingual-e5-small"
]

TOP_K = 3

RANDOM_STATE = 42