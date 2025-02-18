from flask import flash
from app_session.user_session import create_user_session
from conf_enviroment.conf_env import config
from constants.messages import UserMessages
from constants.constants import Constants
from model.article.article_saved import add_saved_article
from model.user.user import add_user, get_user_by_username_password
from model.user.user_email_verify_token import add_email_verify_token, \
    update_token_data_by_user_ag_id
from service.others.mail import send_email
from utils.utility import generate_auto_id, get_response, generate_token, \
    get_current_time_milli_sec

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

    is_article_saved = add_saved_article(user_id, title, description,
                                         article_image_url, url, sentiment)

    if not is_article_saved:
        return get_response(False, '''Failed to save the article''',
                            {}), 500

    flash('''Article saved successfully''', 'success')
    return get_response(True, '''Article saved successfully''', {}), 200
