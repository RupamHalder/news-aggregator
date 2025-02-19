import traceback

from flask import Blueprint, request

from service.web_service.article.article_service import delete_article_service, save_article_service
from utils.utility import get_response
from conf_enviroment.conf_env import config
from constants.messages import CommonMessages
from constants.constants import Constants
from validation.web_validation.article.article_validation import \
    delete_article_field_validation, save_article_field_validation

article_controller = Blueprint('article_controller', __name__)

BASE_URL = config.APP_BASE_URL
TOKEN_EXP_TIME_GAP = Constants.TOKEN_EXP_TIME_GAP
TOKEN_ATTEMPT_TIME_GAP = Constants.TOKEN_ATTEMPT_TIME_GAP
MAXIMUM_TOKEN_REQUEST_COUNT = Constants.MAXIMUM_TOKEN_REQUEST_COUNT


# Routes
@article_controller.route('/save', methods=['POST'])
def save_article():
    try:
        field_validation, status_code = save_article_field_validation(request)
        if field_validation['status']:
            return save_article_service(field_validation['data'])
        else:
            return field_validation, status_code

    except Exception as e:
        print("Error in save_article API: " + str(e))
        print(traceback.format_exc())
        return get_response(False, CommonMessages.FAIL_SOMETHING_WENT_WRONG,
                            {}), 500


@article_controller.route('/delete', methods=['POST'])
def delete_article():
    try:
        field_validation, status_code = delete_article_field_validation(request)
        if field_validation['status']:
            return delete_article_service(field_validation['data'])
        else:
            return field_validation, status_code

    except Exception as e:
        print("Error in delete_article API: " + str(e))
        print(traceback.format_exc())
        return get_response(False, CommonMessages.FAIL_SOMETHING_WENT_WRONG,
                            {}), 500
