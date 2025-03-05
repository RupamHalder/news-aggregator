import traceback

from flask import Blueprint, request, jsonify
from newsapi import NewsApiClient

from conf_enviroment.conf_env import config
from constants.messages import CommonMessages
from service.api.news_api_service import get_country_lang_category_service, get_news_sources_service, get_articles_service
from utils.utility import get_response
from validation.api.news_api_validation import get_articles_field_validation, get_country_lang_category_field_validation, \
    get_news_sources_field_validation

article_api_controller = Blueprint('article_api_controller', __name__)


@article_api_controller.route('/get_sources', methods=['GET'])
def get_sources():
    try:
        field_validation, status_code = get_news_sources_field_validation(
            request)
        if field_validation['status']:
            return get_news_sources_service(field_validation['data'])
        else:
            return field_validation, status_code

    except Exception as e:
        print("Error in get_sources API: " + str(e))
        print(traceback.format_exc())
        return get_response(False, CommonMessages.FAIL_SOMETHING_WENT_WRONG,
                            {}), 500


@article_api_controller.route('/get_articles', methods=['POST'])
def get_articles():
    try:
        field_validation, status_code = get_articles_field_validation(request)
        if field_validation['status']:
            return get_articles_service(field_validation['data'])
        else:
            return field_validation, status_code

    except Exception as e:
        print("Error in delete_article API: " + str(e))
        print(traceback.format_exc())
        return get_response(False, CommonMessages.FAIL_SOMETHING_WENT_WRONG,
                            {}), 500


@article_api_controller.route('/get_country_lang_category', methods=['GET'])
def get_get_country_lang_category():
    try:
        field_validation, status_code = get_country_lang_category_field_validation(
            request)
        if field_validation['status']:
            return get_country_lang_category_service(field_validation['data'])
        else:
            return field_validation, status_code

    except Exception as e:
        print("Error in get_get_country_lang_category API: " + str(e))
        print(traceback.format_exc())
        return get_response(False, CommonMessages.FAIL_SOMETHING_WENT_WRONG,
                            {}), 500
