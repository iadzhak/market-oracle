# Forecast
FRESH_DELTA_MINUTES = 30
MIN_CONFIDENCE = 0
MAX_CONFIDENCE = 0

# Sources
SOURCE_COINGECKO = 'coingecko'
SOURCE_WORLDNEWS = 'worldnews'
SOURCE_BINANCE = 'binance'
SOURCE_NEWSAPI = 'newsapi'

SOURCES = [
    {
        'id': SOURCE_COINGECKO,
        'type': 'Источник цен',
        'url': 'https://www.coingecko.com/'
    },
    {
        'id': SOURCE_WORLDNEWS,
        'type': 'Источник новостей',
        'url': 'https://worldnewsapi.com'
    },
    {
        'id': SOURCE_BINANCE,
        'type': 'Источник цен',
        'url': 'https://www.binance.com/'
    },
    {
        'id': SOURCE_NEWSAPI,
        'type': 'Источник новостей',
        'url': 'https://newsapi.org/'
    },

]