# LLMBox API

Сервис для генерации ответов от AI: OpenAI ChatGPT/Vision, YandexGPT и модели Yandex Foundation (GPT OSS, Qwen). 
Поддерживает обычные и мультимодальные (Vision) запросы.

## Быстрый старт
1. Требования: Python 3.11+, установленные зависимости `pip install -r requirements.txt`.
2. Создайте `.env` рядом с `main.py` и заполните переменные (пример ниже).
3. Запустите: `python main.py` и откройте Swagger по `http://localhost:8001/docs`.

### Переменные окружения
| Переменная | Назначение                                             |
|------------|--------------------------------------------------------|
| `HOST` | Хост (по умолчанию `0.0.0.0`)                          |
| `PORT` | Порт (по умолчанию `8001`)                             |
| `OPENAI_MODEL` | Модель OpenAI (например, `gpt-4.1`)                    |
| `OPENAI_API_KEY` | API-ключ OpenAI                                        |
| `YANDEX_KEY_ID` | ключ сервисного аккаунта                               |
| `YANDEX_SERVICE_ACCOUNT_ID` | `service_account_id`                                   |
| `YANDEX_PRIVATE_KEY` | приватный ключ                                         |
| `YANDEX_GPT_MODEL_PATH` | Префикс модели:`gpt://.../`                            |
| `YANDEX_GPT_API_URL` | `https://llm.api.cloud.yandex.net/foundationModels/v1` |
| `YANDEX_GPT_MODEL_NAME` | Имя модели YandexGPT (например, `yandexgpt/latest`)    |
| `YANDEX_GPT_OSS_120B_MODEL_NAME` | `gpt-oss-120b/latest`                                  |
| `YANDEX_GPT_OSS_20B_MODEL_NAME` | `gpt-oss-20b/latest`                                   |
| `YANDEX_QWEN_235B_MODEL_NAME` | `qwen3-235b-a22b-fp8/latest`                           |
| `YANDEX_OPEN_AI_API_KEY` | Ключ для OpenAI-совместимого API Яндекс                |
| `YANDEX_OPEN_AI_BASE_URL` | `https://llm.api.cloud.yandex.net/v1`                  |

Пример `.env`:
```
HOST=0.0.0.0
PORT=8001

OPENAI_MODEL=gpt-4.1
OPENAI_API_KEY=sk-***

YANDEX_KEY_ID=yc-key-id
YANDEX_SERVICE_ACCOUNT_ID=yc-service-account-id
YANDEX_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
YANDEX_GPT_MODEL_PATH=gpt://folder-id/
YANDEX_GPT_API_URL=https://llm.api.cloud.yandex.net/foundationModels/v1
YANDEX_GPT_MODEL_NAME=yandexgpt/latest
YANDEX_GPT_OSS_120B_MODEL_NAME=gpt-oss-120b/latest
YANDEX_GPT_OSS_20B_MODEL_NAME=gpt-oss-20b/latest
YANDEX_QWEN_235B_MODEL_NAME=qwen3-235b-a22b-fp8/latest
YANDEX_OPEN_AI_API_KEY=yc-openai-key
YANDEX_OPEN_AI_BASE_URL=https://llm.api.cloud.yandex.net/v1
```

### Запуск в Docker
- Локально: `docker build -t llmbox . && docker run -p 8001:8001 --env-file .env llmbox`

## Поддерживаемые LLM
- `chat_gpt` — OpenAI ChatGPT/Vision (использует `OPENAI_MODEL`).
- `yandex_gpt` — облачный YandexGPT.
- `gpt_oss_20b` — Yandex Foundation GPT OSS 20B через OpenAI-совместимый API.
- `gpt_oss_120b` — Yandex Foundation GPT OSS 120B через OpenAI-совместимый API.
- `qwen3_235b` — Yandex Foundation Qwen3 235B через OpenAI-совместимый API.

## Эндпоинты

### 1) POST `/generate-ai-response`
Генерация текстового ответа по истории сообщений.

- Тело: `GenerateAIRequestBody`
- Ответ: `AIResponse`

Тело запроса `GenerateAIRequestBody`:

| Поле       | Тип             | Описание |
|------------|-----------------|----------|
| `messages` | `List[Message]` | История диалога с ролями. |
| `assistant`| `AIAssistant`   | Выбор ассистента/модели. |

`Message`:

| Поле      | Тип    | Описание |
|-----------|--------|----------|
| `role`    | `Role` | `system` \| `user` \| `assistant` |
| `content` | `str`  | Текст сообщения. |

Пример запроса:

```json
POST /generate-ai-response
{
  "messages": [
    {"role": "system", "content": "Вы ИИ-ассистент, помогаете пользователям."},
    {"role": "user", "content": "Привет!"},
    {"role": "assistant", "content": "Здравствуйте! Чем помочь?"},
    {"role": "user", "content": "Как перевести деньги?"}
  ],
  "assistant": "yandex_gpt"
}
```

Пример ответа:

```json
{
  "assistant_message": "Откройте раздел Переводы, выберите получателя и введите сумму.",
  "usage": {"prompt_tokens": 60, "completion_tokens": 20, "total_tokens": 80}
}
```

### 2) POST `/generate-ai-response-vision`
Мультимодальный (Vision) запрос: текст + изображения (под капотом OpenAI Chat Completions Vision).

- Тело: `GenerateVisionAIRequestBody`
- Ответ: `AIResponse`

Тело запроса `GenerateVisionAIRequestBody`:

| Поле       | Тип               | Описание |
|------------|-------------------|----------|
| `messages` | `List[AIMessage]` | Сообщения с массивом контента. |

`AIMessage`:

| Поле      | Тип                                       | Описание          |
|-----------|-------------------------------------------|-------------------|
| `role`    | `Role`                                    | Роль отправителя. |
| `content` | `List[TextContentItem\|ImageContentItem]` | Элементы контента. |

Элементы контента:

- `TextContentItem`: `{ "type": "text", "text": "..." }`
- `ImageContentItem`: `{ "type": "image_url", "image_base64": "data:image/png;base64,..." }`

Пример запроса:

```json
POST /generate-ai-response-vision
{
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Что на картинке?"},
        {"type": "image_url", "image_base64": "data:image/png;base64,iVBORw0K..."}
      ]
    }
  ]
}
```

Пример ответа:

```json
{
  "assistant_message": "На изображении показан график продаж по кварталам...",
  "usage": {"prompt_tokens": 120, "completion_tokens": 45, "total_tokens": 165}
}
```

## Модель ответа

`AIResponse`:

| Поле                | Тип     | Описание |
|---------------------|---------|----------|
| `assistant_message` | `str`   | Сгенерированный ответ. |
| `usage`             | `Usage` | Статистика токенов (может быть `null` в Vision). |

`Usage`:

| Поле               | Тип  | Описание |
|--------------------|------|----------|
| `prompt_tokens`    | `int`| Токенов во входе. |
| `completion_tokens`| `int`| Токенов в ответе. |
| `total_tokens`     | `int`| Всего токенов. |

