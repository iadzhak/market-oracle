from textblob import TextBlob

def calculate_normalized_ma_signal(ohlcv: list[list[float]]) -> float:
    """
    Входные данные должны быть отсортированы в порядке возрастания timestamp.
    Вернет нормализованный сигнал тренда.
    """
    if len(ohlcv) == 0:
        return 0
    closes = [c[4] for c in ohlcv]
    ma = sum(closes) / len(closes)
    return closes[-1] / ma - 1


def calculate_news_sentiment(news: list[str]) -> tuple[float, float]:
    """
    На вход подаются тексты по которым нужно вычислить средний сентимент.
    Возвращает два значения полярность и объективность.
    """
    if len(news) == 0:
        return 0, 0
    p, s = 0, 0
    for n in news:
        testimonial = TextBlob(n)
        p += testimonial.sentiment.polarity
        s += testimonial.sentiment.subjectivity
    return p / len(news), s / len(news)
