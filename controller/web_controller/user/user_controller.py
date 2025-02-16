import traceback

from flask import Blueprint, request

from service.web_service.user.user_service import login_service, \
    register_service
from utils.utility import get_response
from conf_enviroment.conf_env import config
from constants.messages import CommonMessages
from constants.constants import Constants
from validation.web_validation.user.user_validation import \
    register_field_validation, login_field_validation

user_controller = Blueprint('user_controller', __name__)

BASE_URL = config.APP_BASE_URL
TOKEN_EXP_TIME_GAP = Constants.TOKEN_EXP_TIME_GAP
TOKEN_ATTEMPT_TIME_GAP = Constants.TOKEN_ATTEMPT_TIME_GAP
MAXIMUM_TOKEN_REQUEST_COUNT = Constants.MAXIMUM_TOKEN_REQUEST_COUNT


# Routes
@user_controller.route('/register', methods=['POST'])
def register():
    try:
        field_validation, status_code = register_field_validation(request)
        if field_validation['status']:
            return register_service(field_validation['data'])
        else:
            return field_validation, status_code

    except Exception as e:
        print("Error in register API: " + str(e))
        print(traceback.format_exc())
        return get_response(False, CommonMessages.FAIL_SOMETHING_WENT_WRONG,
                            {}), 500


@user_controller.route('/login', methods=['POST'])
def login():
    try:
        field_validation, status_code = login_field_validation(request)
        if field_validation['status']:
            return login_service(field_validation['data'])
        else:
            return field_validation, status_code

    except Exception as e:
        print("Error in register API: " + str(e))
        print(traceback.format_exc())
        return get_response(False, CommonMessages.FAIL_SOMETHING_WENT_WRONG,
                            {}), 500
