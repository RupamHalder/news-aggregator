import traceback

from flask import Blueprint, render_template, request
from textblob import TextBlob
import requests

from conf_enviroment.conf_env import config
from model.user.user import update_is_verified
from model.user.user_email_verify_token import get_token_data_by_token, \
    update_token_data_object
from utils.page_info import get_page_info
from utils.utility import get_current_time_milli_sec

page_controller = Blueprint('page_controller', __name__)

TOKEN_EXP_TIME_GAP = 15 * 60
APP_NAME = config.APP_NAME


# Root Page
@page_controller.route('/')
def index():
    category = request.args.get('category', 'general')
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
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


# Post email verification page
@page_controller.route('/email-verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        token_data = get_token_data_by_token(token)

        if not token_data:
            message = 'Invalid token.'
            message_type = 'error'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))

        if get_current_time_milli_sec() > int(token_data.token_exp_timestamp):
            message = 'The verification link has expired.'
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
            message = 'Unable to verify email.'
            message_type = 'error'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))

        is_verified_updated = update_is_verified(token_data.user_ag_id, True)

        if not is_verified_updated:
            message = 'Unable to verify email.'
            message_type = 'error'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))
        else:
            message = 'Email verified successfully.'
            message_type = 'success'
            return render_template('user/message/email-verify.html',
                                   message=message,
                                   message_type=message_type,
                                   page_info=get_page_info('index'))

    except Exception as e:
        print(traceback.format_exc())
        message = 'Unable to verify email.'
        message_type = 'error'
        return render_template('user/message/email-verify.html',
                               message=message,
                               message_type=message_type,
                               page_info=get_page_info('index'))
