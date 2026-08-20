# 🔮 Market Oracle

Крипто-оракул для предсказания движения цены на основе технических индикаторов и новостного сентимента.
Состоит из двух сервисов: **[frontend](frontend/README.md)** (React/Vite) и **[backend](backend/README.md)** (Python/FastAPI).

## 🚀 Быстрый старт

```bash
cp .env.example .env
touch db.sqlite3
mkdir weights
docker compose up -d --build
```
Для работы системы необходима предварительная тренировка модели. (Создание scaler и default coef/weights).
Без этого шага система не сможет составлять прогноз.


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
# Сколько времени действует прогноз, прежде чем система его обновит
FRESH_DELTA_MINUTES: int = 60
```

> ⚠️ У newsapi.org в бесплатной версии есть ограничение на 100 запросов в день

## 🏋️‍♀️ Предтренировка модели


```bash
docker compose exec backend python -m src.warmup collect
docker compose exec backend python -m src.warmup train
```

Справка по скрипту: `docker compose exec backend python -m src.warmup -h`


## 🏋️ Дотренировка модели

Как только накопилось 5 новых прогнозов система сама дотренируется. Проверка выполнятся после каждого составления нового прогноза.

---

> 📖 Детали по сервисам: [backend/README.md](backend/README.md), [frontend/README.md](frontend/README.md)
