import traceback

from flask import Blueprint, flash, redirect, render_template, request, url_for
from textblob import TextBlob
import requests

from app_session.user_session import destroy_user_session, is_user_logged_in
from conf_enviroment.conf_env import config
from constants.messages import UserMessages
from constants.constants import Constants
from model.user.user import update_is_verified, get_token_data_by_token
from model.user.user_email_verify_token import update_token_data_object
from utils.page_info import get_page_info
from utils.utility import get_current_time_milli_sec

page_controller = Blueprint('page_controller', __name__)

TOKEN_EXP_TIME_GAP = Constants.TOKEN_EXP_TIME_GAP
APP_NAME = config.APP_NAME


# Root Page
@page_controller.route('/')
# @is_user_logged_in("page")
def index():
    category = request.args.get('category', 'general')
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get('articles', [])

    # Add sentiment analysis to each article
    for article in articles:
        analysis = TextBlob(article['description'] or '')
        article['sentiment'] = analysis.sentiment.polarity

    return render_template('index.html',
                           articles=articles,
                           category=category,
                           page_info=get_page_info('index'))

# =================== Before Login ===================
# Login page
@page_controller.route('/login')
def login_page():
    return render_template('user/login.html',
                           page_info=get_page_info('login'))


# Registration page for new users
@page_controller.route('/register')
def registration_page():
    return render_template('user/register.html',
                           page_info=get_page_info('register'))


# Post email verification page
@page_controller.route('/email-verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        token_data = get_token_data_by_token(token)

        if token_data.is_email_verified:
            message = UserMessages.ALREADY_MAIL_VERIFIED
            message_type = 'success'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))

        if not token_data:
            message = UserMessages.INVALID_EMAIL_VERIFY_TOKEN
            message_type = 'error'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))

        if get_current_time_milli_sec() > int(token_data.token_exp_timestamp):
            message = UserMessages.EXPIRED_EMAIL_VERIFY_TOKEN
            message_type = 'error'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))

        token_data.token_exp_timestamp = str(
            int(token_data.token_exp_timestamp) + TOKEN_EXP_TIME_GAP * 1000
        )
        token_data.token_request_count = 0

        is_token_updated = update_token_data_object(token_data)
        if not is_token_updated:
            message = UserMessages.FAIL_VERIFY_MAIL
            message_type = 'error'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))

        is_verified_updated = update_is_verified(token_data.user_ag_id, True)

        if not is_verified_updated:
            message = UserMessages.FAIL_VERIFY_MAIL
            message_type = 'error'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))
        else:
            message = UserMessages.SUCCESS_VERIFY_MAIL
            message_type = 'success'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))

    except Exception as e:
        print(traceback.format_exc())
        message = UserMessages.FAIL_VERIFY_MAIL
        message_type = 'error'
        return render_template('user/message/email-verify.html',
                               message=message,
                               message_type=message_type,
                               page_info=get_page_info('index'))
    

# Registration page for new users
@page_controller.route('/logout')
def logout_page():
    destroy_user_session()
    flash(UserMessages.SUCCESS_USER_LOGOUT, 'success')
    return redirect(url_for('page_controller.login_page'))
