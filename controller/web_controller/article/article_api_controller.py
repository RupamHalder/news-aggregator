from flask import Blueprint, request, session, jsonify
from newsapi import NewsApiClient

from conf_enviroment.conf_env import config
from utils.utility import get_response

article_api_controller = Blueprint('article_api_controller', __name__)

# Initialize News API client
NEWS_API_KEY = config.NEWS_API_KEY
newsapi = NewsApiClient(api_key=NEWS_API_KEY)


@article_api_controller.route('/get_sources', methods=['GET'])
def get_sources():
    sources = newsapi.get_sources()['sources']  # Retrieve available sources
    if len(sources) == 0:
        return jsonify(get_response(False, 'No sources found', [])), 404

    return jsonify(get_response(True, 'Sources retrieved successfully', sources)), 200


@article_api_controller.route('/get_articles', methods=['GET'])
def get_articles():
    selected_sources = request.args.get('sources')
    if not selected_sources:
        return jsonify(get_response(False, 'No sources selected', []))

    selected_sources = ','.join(selected_sources.split(','))  # Format sources list
    articles = newsapi.get_top_headlines(sources=selected_sources)
    return jsonify(articles['articles'])

