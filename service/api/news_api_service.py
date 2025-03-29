import json
from textblob import TextBlob
import requests
from newsapi import NewsApiClient
from flask import url_for

from app_session.user_session import is_logged_in_user
from conf_enviroment.conf_env import config
from constants.constants import Constants
from utils.utility import get_response, is_param_empty
from constants.messages import ArticleMessages, CommonMessages

# Initialize News API client
NEWS_API_KEY = config.NEWS_API_KEY
newsapi = NewsApiClient(api_key=NEWS_API_KEY)


# category=None, language=None, country=None
def get_news_sources_service(cleaned_data):
    page = cleaned_data.get('page')
    q = cleaned_data.get('q')

    params = {
        'language': cleaned_data.get('language'),
        'country': cleaned_data.get('country'),
        'category': cleaned_data.get('category')
    }

    sources = newsapi.get_sources(**params)['sources']  # Retrieve available sources
    if len(sources) == 0:
        return get_response(False, ArticleMessages.NOT_FOUND_SOURCES, []), 404
    
    if not is_param_empty(q):
        sources = [s for s in sources if q in s.get('name')]

    start_index = 10 * (page - 1)
    end_index = 10 * page
    formatted_list = [{
        "id": s.get('id'),
        "text": s.get('name')
    } for s in sources[start_index: end_index]]

    response = get_response(True, ArticleMessages.SUCCESS_SOURCE_FETCH,
                            formatted_list)
    response["count"] = len(sources)

    return response, 200


def get_country_lang_category_service(cleaned_data):
    page = cleaned_data.get('page')
    q = cleaned_data.get('q')
    resource_type = cleaned_data.get('resource_type')
    if resource_type == "country":
        sources = Constants.COUNTRY_CODE
    elif resource_type == "language":
        sources = Constants.LANGUAGE_CODE
    elif resource_type == "category":
        sources = Constants.NEWS_CATEGORY
    else:
        return get_response(False, 'Invalid resource type!', []), 404

    if len(sources) == 0:
        return get_response(False, CommonMessages.NOT_FOUND_DATA, []), 404
    
    if not is_param_empty(q):
        sources = [s for s in sources if q.lower() in s.get('text').lower()]

    start_index = 10 * (page - 1)
    end_index = 10 * page
    response = get_response(True, ArticleMessages.SUCCESS_SOURCE_FETCH,
                            sources[start_index: end_index])
    response["count"] = len(sources)

    return response, 200


def get_articles_service(cleaned_data):
    sources = cleaned_data.get('sources')

    params = {
        'sources': ','.join(sources),
        'q': cleaned_data.get('news_query'),
        'language': cleaned_data.get('language'),
        # 'country': cleaned_data.get('country'),
        # 'category': cleaned_data.get('category'),
        'page_size': cleaned_data.get('page_size'),
        'page': cleaned_data.get('page'),
    }

    articles = newsapi.get_top_headlines(**params)
    print(articles["articles"])
    for article in articles:
        article['urlToImage'] = article['urlToImage'] if article['urlToImage'] else url_for('static', filename='assets/img/no-image.jpg')
        article['publishedAt'] = article['publishedAt'].split('T')[0]
    return get_response(True, ArticleMessages.SUCCESS_ARTICLE_FETCH,
                        {
                            'articles': articles['articles'],
                            'is_logged_in': is_logged_in_user()
                        }), 200


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
