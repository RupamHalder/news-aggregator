from textblob import TextBlob
import requests

from conf_enviroment.conf_env import config


def get_articles_with_sentiment_by_category(category):
    # Implement the logic to get articles by category from the NewsAPI
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get('articles', [])

    # Add sentiment analysis to each article
    for article in articles:
        analysis = TextBlob(article['description'] or '')
        article[
            'sentiment'] = 'Positive' if analysis.sentiment.polarity > 0 else \
            'Negative' if analysis.sentiment.polarity < 0 else 'Neutral'