# Forecast
FRESH_DELTA_MINUTES = 30
MIN_CONFIDENCE = 0
MAX_CONFIDENCE = 0

# Sources
SOURCE_COINGECKO = 'coingecko'
SOURCE_CRYPTOPANIK = 'cryptopanic'

SOURCES = [
    {
        'id': SOURCE_COINGECKO,
        'type': 'Источник цен',
        'url': 'https://www.coingecko.com/'
    },
    {
        'id': 'cryptopanic',
        'type': 'Источник новостей',
        'url': 'https://cryptopanic.com/'
    }
]