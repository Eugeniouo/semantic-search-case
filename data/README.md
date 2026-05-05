# Датасет «Навигатор по смыслу» — v1.0

**Чемпионат ГК «Ростелеком» | Направление: Искусственный интеллект | Кейс 1 | 2026**

---

## Описание датасета

Датасет предназначен для разработки и оценки системы семантического поиска по корпусу программного кода (кейс «Навигатор по смыслу», версия 1.0). Он включает 200 функций на Python и Java, сгруппированных по 5 тематическим категориям, и 25 тестовых вопросов на русском и английском языках. Задача участников — построить retrieval-систему, которая по текстовому запросу возвращает наиболее релевантные функции из корпуса. Датасет единый для всех команд чемпионата: это гарантирует сопоставимость метрик (Precision@3, MRR) между участниками и исключает влияние различий в данных на итоговый рейтинг.

---

## Структура датасета

```
dataset_v1.0/
├── categories.json       # 5 категорий кода
├── code_corpus.json      # 200 функций (100 Python + 100 Java)
└── eval_questions.json   # 25 тестовых вопросов с эталонными ответами
```

---

## Описание файлов

### categories.json

Справочник категорий. Содержит 5 записей.

**Схема верхнего уровня:**

```json
{
  "version": "1.0",
  "categories": [...]
}
```

**Поля каждой категории:**

| Поле | Тип | Описание |
|------|-----|----------|
| `key` | string | Уникальный идентификатор категории |
| `label` | string | Человекочитаемое название |
| `color` | string | HEX-цвет для визуализации |
| `description` | string | Краткое описание содержимого категории |

**Пример записи:**

```json
{
  "key": "auth",
  "label": "Аутентификация и авторизация",
  "color": "#E74C3C",
  "description": "Функции для проверки пользователя, работы с токенами, сессиями и правами доступа."
}
```

---

### code_corpus.json

Корпус функций для индексирования. Содержит 200 записей в виде массива JSON.

**Поля каждой функции:**

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | string | Уникальный идентификатор: `func_001` … `func_200` |
| `language` | string | Язык программирования: `python` или `java` |
| `function_name` | string | Имя функции/метода |
| `code` | string | Исходный код функции |
| `description` | string | Описание назначения функции на русском языке |
| `category` | string | Ключ категории из `categories.json` |

**Распределение по языкам:**

- `func_001` – `func_100` → `language: "python"`
- `func_101` – `func_200` → `language: "java"`

**Пример записи:**

```json
{
  "id": "func_001",
  "language": "python",
  "function_name": "verify_jwt_token",
  "code": "def verify_jwt_token(token: str, secret: str) -> dict:\n    \"\"\"Проверяет JWT-токен и возвращает payload или причину невалидности.\"\"\"\n    try:\n        payload = jwt.decode(token, secret, algorithms=[\"HS256\"])\n        return {\"valid\": True, \"data\": payload}\n    except jwt.ExpiredSignatureError:\n        return {\"valid\": False, \"error\": \"expired\"}\n    except jwt.InvalidTokenError:\n        return {\"valid\": False, \"error\": \"invalid\"}",
  "description": "Проверяет JWT-токен и возвращает payload или причину невалидности.",
  "category": "auth"
}
```

---

### eval_questions.json

Тестовые вопросы для оценки качества retrieval. Содержит 25 записей в виде массива JSON.

**Поля каждого вопроса:**

| Поле | Тип | Описание |
|------|-----|----------|
| `question_id` | string | Уникальный идентификатор: `q_01` … `q_25` |
| `query` | string | Поисковый запрос на естественном языке |
| `language` | string | Язык запроса: `ru` или `en` |
| `correct_chunk_id` | string | ID эталонной функции из `code_corpus.json` |

**Пример записи:**

```json
{
  "question_id": "q_01",
  "query": "как проверить, истёк ли токен?",
  "language": "ru",
  "correct_chunk_id": "func_001"
}
```

---

## Категории кода

| Ключ | Название | Цвет | Описание |
|------|----------|------|----------|
| `auth` | Аутентификация и авторизация | `#E74C3C` | JWT, пароли, сессии, OAuth, 2FA, права доступа |
| `database` | Работа с базой данных | `#3498DB` | CRUD, транзакции, миграции, индексы, bulk-операции |
| `http` | HTTP-клиенты и API | `#2ECC71` | REST-вызовы, retry, webhook, upload, кэширование |
| `validation` | Валидация и парсинг | `#F39C12` | email, телефон, ИНН, СНИЛС, ISO-даты, URL |
| `utils` | Утилиты и хелперы | `#9B59B6` | форматирование, кэш, slugify, sanitize |

---

## Загрузка данных в Python

Минимальный пример чтения всех трёх файлов:

```python
import json

with open("code_corpus.json", encoding="utf-8") as f:
    corpus = json.load(f)

with open("eval_questions.json", encoding="utf-8") as f:
    questions = json.load(f)

with open("categories.json", encoding="utf-8") as f:
    categories = json.load(f)["categories"]

print(len(corpus))      # 200
print(len(questions))   # 25
print(len(categories))  # 5
```

Доступ к полям:

```python
# Первая функция в корпусе
func = corpus[0]
print(func["id"])             # func_001
print(func["language"])       # python
print(func["function_name"])  # verify_jwt_token
print(func["category"])       # auth

# Первый вопрос
q = questions[0]
print(q["question_id"])       # q_01
print(q["query"])             # как проверить, истёк ли токен?
print(q["correct_chunk_id"])  # func_001
```

---

## Инструкция по самопроверке

Запустите скрипт из директории `dataset_v1.0/` перед началом работы, чтобы убедиться в целостности данных:

```python
import json

corpus = json.load(open("code_corpus.json", encoding="utf-8"))
questions = json.load(open("eval_questions.json", encoding="utf-8"))
cats = json.load(open("categories.json", encoding="utf-8"))["categories"]

assert len(corpus) == 200, f"corpus: {len(corpus)}"
assert len(questions) == 25, f"questions: {len(questions)}"
assert len(cats) == 5, f"categories: {len(cats)}"

ids = [f["id"] for f in corpus]
assert len(ids) == len(set(ids)), "duplicate ids"

corpus_ids = set(ids)
for q in questions:
    assert q["correct_chunk_id"] in corpus_ids, f"missing: {q['correct_chunk_id']}"

for f in corpus[:100]:
    assert f["language"] == "python"
for f in corpus[100:]:
    assert f["language"] == "java"

print("✓ Все проверки пройдены")
```

Скрипт проверяет:

- JSON-файлы валидны и читаются без ошибок
- Корпус содержит ровно 200 функций
- Набор вопросов содержит ровно 25 записей
- Справочник содержит ровно 5 категорий
- Отсутствие дублирующихся `id` в корпусе
- Все `correct_chunk_id` из вопросов присутствуют в корпусе
- `func_001`–`func_100` имеют `language == "python"`, `func_101`–`func_200` — `language == "java"`

---

## Метрики оценки

Retrieval-система оценивается по двум метрикам на наборе `eval_questions.json`:

### Precision@3

Доля запросов, для которых эталонная функция вошла в топ-3 результатов поиска.

```
Precision@3 = (число запросов, где correct_chunk_id ∈ top-3) / 25
```

### MRR (Mean Reciprocal Rank)

Среднее обратное значение позиции эталонной функции в результатах.

```
MRR = (1/25) * Σ (1 / rank_i)
```

где `rank_i` — позиция `correct_chunk_id` в ответе для запроса `i` (если не найден, вклад = 0).

---

## Что не входит в датасет

- **Нет обучающего (train) набора.** Датасет предназначен исключительно для индексирования корпуса и оценки retrieval-качества.
- **Нет разбивки train/test по функциям.** Все 200 функций индексируются; по 25 вопросам считаются метрики.
- **Нет предвычисленных эмбеддингов.** Выбор модели для построения векторных представлений — на усмотрение команды.
- **Нет ограничений на стек.** Участники свободны в выборе библиотек, моделей и способа хранения индекса.

---

## Версионирование

| Версия | Дата | Изменения |
|--------|------|-----------|
| 1.0 | 2026 | Первый публичный выпуск датасета |

Текущая версия: **1.0**. При обновлениях будет создана новая директория `dataset_v1.x/` с собственным `README.md`.

---

## Контакт

По вопросам о датасете обращайтесь к организаторам чемпионата ГК «Ростелеком» через официальные каналы направления «Искусственный интеллект».
