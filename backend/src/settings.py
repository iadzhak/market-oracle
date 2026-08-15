from pydantic_settings import BaseSettings

DEFAULT_TOKENS = {
    'bitcoin', 'ethereum', 'solana',
    'binancecoin', 'cardano', 'ripple' 'dogecoin',
    'tontoken'
}


class Settings(BaseSettings):
    AVAILABLE_TOKENS: set[str] = DEFAULT_TOKENS  # id from coingecko

    COINGECKO_API_KEY: str = 'CG-PepHaJMtCeuzCxdswZAM5Em7'
    COINGECKO_API_URL: str = 'https://api.coingecko.com/api/v3'

    DB_URL: str = 'sqlite+aiosqlite:///db.sqlite3'

    model_config = {'env_file': '.env', 'env_file_encoding': 'utf-8'}


conf = Settings()

def get_settings() -> Settings:
    return Settings()


class CoinGeckoURLs:
    coins_list = '/coins/list'
    history = '/coins/{id}/ohlc'