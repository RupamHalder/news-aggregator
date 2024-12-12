from flask import Blueprint, render_template, request
from textblob import TextBlob
import requests

from conf_enviroment.conf_env import config
from utils.page_info import get_page_info

APP_NAME = config.APP_NAME

page_controller = Blueprint('page_controller', __name__)


@page_controller.route('/')
def index():
    category = request.args.get('category', 'general')
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
    # print("\n\n===============================")
    # print(response.json())
    # print("===============================\n\n")
    articles = response.json().get('articles', [])

    # Add sentiment analysis to each article
    for article in articles:
        analysis = TextBlob(article['description'] or '')
        article[
            'sentiment'] = 'Positive' if analysis.sentiment.polarity > 0 else \
            'Negative' if analysis.sentiment.polarity < 0 else 'Neutral'

    return render_template('index.html',
                           articles=articles,
                           category=category,
                           page_info=get_page_info('index'))
