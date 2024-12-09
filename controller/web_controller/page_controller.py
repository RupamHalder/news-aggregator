from flask import Blueprint, render_template, request
from textblob import TextBlob
import requests

from conf_enviroment.conf_env import config

page_controller = Blueprint('page_controller', __name__)


@page_controller.route('/dashboard')
def dashboard():
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
            'sentiment'] = 'Positive' if analysis.sentiment.polarity > 0 else 'Negative' if analysis.sentiment.polarity < 0 else 'Neutral'

    return render_template('dashboard.html', articles=articles,
                           category=category)
