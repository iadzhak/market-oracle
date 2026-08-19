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
# Токены для прогноза (JSON array).
# Принятые наименования токенов
# Посмотреть например тут: https://www.binance.com/ru/markets/overview
TOKENS='["BTC", "ETH", "BNB", "SOL"]'

# Новости (NewsAPI) 
# Получить api key можно тут: https://newsapi.org/
NEWS_API_KEY=your-api-key
# Если с api проблемы то можно включить мок на новости
# Мок включен по умолчанию, поэтому его надо обязательно отключить при использовании новостного api
NEWS_FAKER=True
```

## 📦 Предтренировка модели

```bash
docker compose exec backend python -m src.warmup collect
docker compose exec backend python -m src.warmup train
```

---

> 📖 Детали по сервисам: [backend/README.md](backend/README.md), [frontend/README.md](frontend/README.md)
