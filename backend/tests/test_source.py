import datetime as dt
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.sources.ccxt_getter import CCXTPriceGetter
from src.sources.newsapi_getter import NewsApiGetter


class TestCCXTPriceGetter:
    def setup_method(self):
        self.getter = CCXTPriceGetter('binance')
        self.getter.exchange = MagicMock()

    @pytest.mark.asyncio
    async def test_get_ohlcv_1h(self):
        mock_data = [
            [1609459200000, 1.0, 2.0, 0.5, 1.5, 100],
            [1609462800000, 1.5, 2.5, 1.0, 2.0, 120],
        ]
        self.getter.exchange.fetch_ohlcv = AsyncMock(return_value=mock_data)
        
        result = await self.getter.get_ohlcv_1h('bitcoin', dt.datetime.now(), 2)
        
        assert result == mock_data
        self.getter.exchange.fetch_ohlcv.assert_called_once()

    def test_parse_close_prices(self):
        data = [
            [1609459200000, 10, 20, 5, 15, 100],
            [1609462800000, 15, 25, 10, 20, 120],
        ]
        result = self.getter.parse_close_prices(data)
        assert result == [15, 20]

    def test_calculate_normalized_ma(self):
        prices = [10, 20, 30]
        ma = sum(prices) / len(prices)
        expected = prices[-1] / ma - 1
        result = self.getter.calculate_normalized_ma(prices)
        assert result == expected

    def test_calculate_normalized_ma_empty(self):
        result = self.getter.calculate_normalized_ma([])
        assert result == 0

    def test_parce_close_price_last(self):
        data = [
            [1609459200000, 10, 20, 5, 15, 100],
            [1609462800000, 15, 25, 10, 20, 120],
        ]
        result = self.getter.parce_close_price_last(data)
        assert result == 20


class TestNewsApiGetter:
    @pytest.fixture
    def getter(self):
        return NewsApiGetter(
            base_url="https://newsapi.org",
            api_key="test_key",
            news_url="/v2/everything"
        )

    @pytest.mark.asyncio
    async def test_get_news(self, getter):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'ok',
            'articles': [
                {
                    'title': 'BTC rises',
                    'description': 'Bitcoin price increased significantly today'
                }
            ]
        }

        getter.client.get = AsyncMock(return_value=mock_response)

        result = await getter.get_news('BTC', dt.datetime(2025, 1, 1))

        assert result['status'] == 'ok'
        assert len(result['articles']) == 1
        getter.client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_news_default_date(self, getter):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'ok', 'articles': []}
        getter.client.get = AsyncMock(return_value=mock_response)

        result = await getter.get_news('ETH')

        assert result['status'] == 'ok'
        call_args = getter.client.get.call_args
        call_params = call_args.kwargs.get('params', call_args[1].get('params', {}))
        assert 'q' in call_params
        assert call_params['q'] == 'eth token'
        assert call_params['pageSize'] == 10
        assert call_params['language'] == 'en'
        assert call_params['sortBy'] == 'publishedAt'

    def test_calculate_news_sentiment_positive(self):
        with patch('src.sources.newsapi_getter.TextBlob') as MockBlob:
            instance = MockBlob.return_value
            instance.sentiment.polarity = 0.5
            instance.sentiment.subjectivity = 0.6

            news = ['Great positive news', 'Very positive development']
            pol, subj = NewsApiGetter('', '', '').calculate_news_sentiment(news)

            assert pol == 0.5
            assert subj == 0.6
            assert MockBlob.call_count == 2

    def test_calculate_news_sentiment_negative(self):
        with patch('src.sources.newsapi_getter.TextBlob') as MockBlob:
            instance = MockBlob.return_value
            instance.sentiment.polarity = -0.5
            instance.sentiment.subjectivity = 0.7

            news = ['Bad market crash', 'Terrible losses reported']
            pol, subj = NewsApiGetter('', '', '').calculate_news_sentiment(news)

            assert pol == -0.5
            assert subj == 0.7

    def test_calculate_news_sentiment_mixed(self):
        with patch('src.sources.newsapi_getter.TextBlob') as MockBlob:
            def side_effect(*args):
                mock_instance = MagicMock()
                # Alternating polarity: 0.4, -0.2 => avg = 0.1
                # Alternating subjectivity: 0.5, 0.3 => avg = 0.4
                if args and 'positive' in args[0].lower():
                    mock_instance.sentiment.polarity = 0.4
                    mock_instance.sentiment.subjectivity = 0.5
                else:
                    mock_instance.sentiment.polarity = -0.2
                    mock_instance.sentiment.subjectivity = 0.3
                return mock_instance

            MockBlob.side_effect = side_effect

            news = ['Positive market trend', 'Negative regulation fear']
            pol, subj = NewsApiGetter('', '', '').calculate_news_sentiment(news)

            assert pol == 0.1
            assert subj == 0.4

    def test_calculate_news_sentiment_empty(self):
        pol, subj = NewsApiGetter('', '', '').calculate_news_sentiment([])
        assert pol == 0
        assert subj == 0

    def test_parse_articles(self):
        data = {
            'articles': [
                {'description': 'First article description'},
                {'description': 'Second article description'},
                {'description': 'Third article description'},
            ]
        }
        result = NewsApiGetter('', '', '').parse_articles(data)
        assert len(result) == 3
        assert result[0] == 'First article description'
        assert result[1] == 'Second article description'
        assert result[2] == 'Third article description'

    def test_parse_articles_empty(self):
        data = {'articles': []}
        result = NewsApiGetter('', '', '').parse_articles(data)
        assert result == []

    def test_parse_articles_missing_articles_key(self):
        data = {'status': 'ok'}
        result = NewsApiGetter('', '', '').parse_articles(data)
        assert result == []
