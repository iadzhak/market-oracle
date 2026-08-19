# 🔮 Крипто Оракул

Фронтенд часть проекта **Крипто Оракул** — интерактивное гадание на картах Таро для криптовалют.

## 🚀 Технологии

- **React** + **TypeScript**
- **Vite**
- **ESLint**
- **Docker** + **Nginx**

Источники:
- иконки токенов — [cryptoicon.io](https://cryptoicon.io)
- стрелки — [icons8.com](https://icons8.com)

## 📦 Запуск

### Установка зависимостей

```bash
npm install
```

### Dev-режим

```bash
npm run dev
```

Сервер запустится на `http://localhost:5173` и автоматически обновится при изменении файлов.

### Сборка для продакшена

```bash
npm run build
```

### Просмотр сборки

```bash
npm run preview
```

### Линтинг

```bash
npm run lint
```

## 🐳 Docker

Проект поддерживает контейнеризацию с использованием двух стадий:
1. **Node** — установка зависимостей и сборка проекта
2. **Nginx** — раздача статических файлов и проксирование API-запросов

### Сборка и запуск

```bash
docker build -t crypto-oracle-frontend .
docker run -p 80:80 crypto-oracle-frontend
```

### Конфигурация Nginx

- Раздача статических файлов из `/usr/share/nginx/html`
- Проксирование API-запросов с `/api/` на бэкенд (`backend:8000`)
- Проксирование Swagger-документации с `/docs` на бэкенд
- History fallback для SPA (`try_files` на `index.html`)

## 📁 Структура проекта

```
src/
├── components/          # React-компоненты
│   ├── AlertCard.tsx    # Компонент уведомления о рисках
│   └── TarotCard.tsx    # Компонент карты Таро
├── assets/              # Статические ресурсы (изображения, звуки)
├── App.tsx              # Корневой компонент
├── api.ts               # API-маршруты
└── main.tsx             # Точка входа
```

## ⚙️ Скрипты

| Скрипт | Описание |
|--------|----------|
| `npm run dev` | Запуск dev-сервера |
| `npm run build` | Сборка для продакшена (tsc + vite) |
| `npm run preview` | Превью продакшен-сборки |
| `npm run lint` | Запуск ESLint |
