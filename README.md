# 🔮 Market Oracle

Крипто-оракул для предсказания движения цены на основе технических индикаторов и новостного sentiments'a.

## 🚀 Быстрый старт

```bash
touch db.sqlite3
docker compose up -d --build
```

- **Frontend**: http://localhost
- **Backend API**: http://localhost/api/
- **Swagger**: http://localhost/docs

## ⚙️ Переменные окружения

Создай `.env` в корне проекта:

```bash
# Токены для прогноза (JSON array)
TOKENS='["BTC", "ETH", "BNB", "SOL"]'

# Новости (NewsAPI)
NEWS_API_KEY=your-api-key
NEWS_FAKER=false          # true = фейковые новости (без API)
```

## 📦 Предтренировка модели

```bash
docker compose exec backend python -m src.warmup collect
docker compose exec backend python -m src.warmup train
```

---

> 📖 Детали по сервисам: [backend/README.md](backend/README.md), [frontend/README.md](frontend/README.md)
