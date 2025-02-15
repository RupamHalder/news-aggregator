from flask import flash
from app_session.user_session import create_user_session
from constants.messages import UserMessages
from model.user.user import add_user, get_user_by_username_password
from model.user.user_email_verify_token import add_email_verify_token
from service.others.mail import send_email
from utils.utility import generate_auto_id, get_response, generate_token, \
    get_current_time_milli_sec

BASE_URL = "http://localhost:5001/"
TOKEN_EXP_TIME_GAP = 15 * 60
TOKEN_ATTEMPT_TIME_GAP = 5 * 60
MAXIMUM_TOKEN_REQUEST_COUNT = 3


def register_service(cleaned_data):
    email = cleaned_data.get('email')
    password = cleaned_data.get('password')

    user_ag_id = generate_auto_id(prefix="user", length=32)
    is_user_added = add_user(user_ag_id=user_ag_id, username=email,
                             password=password)

    if not is_user_added:
        return get_response(False, UserMessages.FAIL_USER_REGISTRATION,
                            {}), 500

    token = generate_token(32)
    token_exp_timestamp = str(
        get_current_time_milli_sec() + TOKEN_EXP_TIME_GAP * 1000)
    token_request_count = 1
    next_token_request_timestamp = str(
        get_current_time_milli_sec() + TOKEN_ATTEMPT_TIME_GAP * 1000)

    is_token_added = add_email_verify_token(user_ag_id, token,
                                            token_exp_timestamp,
                                            token_request_count,
                                            next_token_request_timestamp)

    if not is_token_added:
        return get_response(False, UserMessages.FAIL_USER_REGISTRATION,
                            {}), 500

    verification_link = f"{BASE_URL}/email-verify/{token}"
    email_body = f"Click the link to verify your email: {verification_link}"

    is_email_sent = send_email('Verify Your Email', email, email_body)

    if not is_email_sent:
        return get_response(False, UserMessages.FAIL_VERIFY_MAIL_SEND, {}), 500

    return get_response(True, UserMessages.SUCCESS_USER_REGISTRATION, {}), 200


def login_service(cleaned_data):
    email = cleaned_data.get('email')
    password = cleaned_data.get('password')

    user_data = get_user_by_username_password(email, password)
    print("user_data: ", user_data)
    if user_data is not None:
        create_user_session(user_data)
        flash(UserMessages.SUCCESS_USER_LOGIN, 'success')
        return get_response(True, UserMessages.SUCCESS_USER_LOGIN, {}), 200
    else:
        flash(UserMessages.FAIL_USER_LOGIN, 'error')
        return get_response(False, UserMessages.FAIL_USER_LOGIN, {}), 400
