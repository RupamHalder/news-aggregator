import traceback

from flask import Blueprint, request

from service.web_service.article.article_service import save_article_service
from service.web_service.user.user_service import login_service, \
    register_service
from utils.utility import get_response
from conf_enviroment.conf_env import config
from constants.messages import CommonMessages
from constants.constants import Constants
from validation.web_validation.article.article_validation import \
    save_article_field_validation
from validation.web_validation.user.user_validation import \
    register_field_validation, login_field_validation

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
