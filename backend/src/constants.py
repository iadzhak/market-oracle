# Forecast
FRESH_DELTA_MINUTES = 30
MIN_CONFIDENCE = 0
MAX_CONFIDENCE = 0

# Sources
SOURCE_BINANCE = 'binance'
SOURCE_NEWSAPI = 'newsapi'

SOURCES = [
    {
        'id': SOURCE_BINANCE,
        'type': 'Источник цен',
        'url': 'https://www.binance.com/'
    },
    {
        'id': SOURCE_NEWSAPI,
        'type': 'Источник новостей',
        'url': 'https://newsapi.org/'
    }
]
