from flask import flash
from conf_enviroment.conf_env import config
from constants.messages import ArticleMessages
from constants.constants import Constants
from model.article.article_saved import add_saved_article, \
    update_article_table_single_row_data
from utils.utility import get_response

BASE_URL = config.APP_BASE_URL
TOKEN_EXP_TIME_GAP = Constants.TOKEN_EXP_TIME_GAP
TOKEN_ATTEMPT_TIME_GAP = Constants.TOKEN_ATTEMPT_TIME_GAP
MAXIMUM_TOKEN_REQUEST_COUNT = Constants.MAXIMUM_TOKEN_REQUEST_COUNT


def save_article_service(cleaned_data):
    user_id = cleaned_data.get('user_id')
    title = cleaned_data.get('title')
    url = cleaned_data.get('url')
    description = cleaned_data.get('description')
    article_image_url = cleaned_data.get('article_image_url')
    sentiment = cleaned_data.get('sentiment')
    published_at = cleaned_data.get('published_at')

    is_article_saved = add_saved_article(user_id, title, description,
                                         article_image_url, url, sentiment,
                                         published_at)

    if not is_article_saved:
        return get_response(False, ArticleMessages.FAIL_SAVE_ARTICLE,
                            {}), 500

    flash(ArticleMessages.SUCCESS_SAVE_ARTICLE, 'success')
    return get_response(True, ArticleMessages.SUCCESS_SAVE_ARTICLE, {}), 200


def delete_article_service(cleaned_data):
    saved_article_id = cleaned_data.get('saved_article_id')

    is_article_saved = update_article_table_single_row_data(
        [saved_article_id], ['saved_article_ag_id'],
        {"is_deleted": True, "status": False})

    if not is_article_saved:
        return get_response(False, ArticleMessages.FAIL_DELETE_ARTICLE,
                            {}), 500

    flash(ArticleMessages.SUCCESS_DELETE_ARTICLE, 'success')
    return get_response(True, ArticleMessages.SUCCESS_DELETE_ARTICLE, {}), 200
