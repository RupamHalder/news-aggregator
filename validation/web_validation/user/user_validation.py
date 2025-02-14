from constants.messages import UserMessages, CommonMessages
from model.user.user import is_username_exist
from utils.utility import get_response, is_email_valid, \
    check_password_validity, is_param_empty


def register_field_validation(request):
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if is_param_empty(email) or is_param_empty(password):
        return get_response(False, UserMessages.REQUIRE_EMAIL_PASS, {}), 400

    if not is_email_valid(email):
        return get_response(False, UserMessages.INVALID_EMAIL, {}), 400

    if is_username_exist(email):
        return get_response(False, UserMessages.EXISTS_EMAIL, {}), 400

    is_password_valid, message = check_password_validity(password)
    if not is_password_valid:
        return get_response(False, message, {}), 400

    return get_response(True, CommonMessages.SUCCESS, {
        "email": email,
        "password": password
    }), 200


def login_field_validation(request):
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if is_param_empty(email) or is_param_empty(password):
        return get_response(False, UserMessages.REQUIRE_EMAIL_PASS, {}), 400

    if not is_email_valid(email):
        return get_response(False, UserMessages.INVALID_EMAIL, {}), 400

    if not is_username_exist(email):
        return get_response(False, UserMessages.NOT_EXISTS_EMAIL, {}), 400

    is_password_valid, message = check_password_validity(password)
    if not is_password_valid:
        return get_response(False, message, {}), 400

    return get_response(True, CommonMessages.SUCCESS, {
        "email": email,
        "password": password
    }), 200
