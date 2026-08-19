from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    TOKENS: set[str] = {'BTC', 'ETH', 'BNB', 'DOGE', 'SOL', 'XRP', 'ONDO'}

    NEWS_FAKER: bool = True
    NEWS_API_KEY: str = 'secret-key'
    NEWS_API_URL: str = 'https://newsapi.org/v2'
    NEWS_API_ENDPOINT: str = '/everything'

    CCXT_EXCHANGE: str = 'binance'

    DB_URL: str = 'sqlite+aiosqlite:///db.sqlite3'

    DEFAULT_MODEL_NAME: str = 'default'

    DELTA_DAYS_PREDICT: int = 1
    FRESH_DELTA_MINUTES: int = 1  # 60


conf = Settings()
