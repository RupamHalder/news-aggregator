from flask import flash
from app_session.user_session import create_user_session
from conf_enviroment.conf_env import config
from constants.messages import UserMessages
from constants.constants import Constants
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

    flash(UserMessages.SUCCESS_USER_REGISTRATION, 'success')
    return get_response(True, UserMessages.SUCCESS_USER_REGISTRATION, {}), 200


def login_service(cleaned_data):
    email = cleaned_data.get('email')
    password = cleaned_data.get('password')

    user_data = get_user_by_username_password(email, password)
    if user_data is None:
        return get_response(False, UserMessages.FAIL_USER_LOGIN, {}), 400

    if user_data.get('is_verified'):
        create_user_session(user_data.get('user_data'))
        flash(UserMessages.SUCCESS_USER_LOGIN, 'success')
        return get_response(True, UserMessages.SUCCESS_USER_LOGIN,
                            {"home_page_redirection": True}), 200

    verification_data = user_data.get('email_verification_data')
    verification_token = verification_data.get('token')
    token_request_count = verification_data.get('token_request_count')
    next_token_request_timestamp = verification_data.get(
        'next_token_request_timestamp')
    user_detail = user_data.get('user_data')
    user_ag_id = user_detail.get('user_id')
    if verification_token is None:
        token = generate_token(32)
        token_exp_timestamp = str(
            get_current_time_milli_sec() + TOKEN_EXP_TIME_GAP * 1000)
        token_request_count = 1
        next_token_request_timestamp = str(
            get_current_time_milli_sec() + TOKEN_ATTEMPT_TIME_GAP * 1000)

        is_token_add_or_updated = add_email_verify_token(user_ag_id,
                                                         token,
                                                         token_exp_timestamp,
                                                         token_request_count,
                                                         next_token_request_timestamp)
    else:
        if get_current_time_milli_sec() < int(
                next_token_request_timestamp
        ) or token_request_count >= MAXIMUM_TOKEN_REQUEST_COUNT:
            return get_response(False,
                                UserMessages.PLEASE_VERIFY_MAIL,
                                {}), 400
        token = generate_token(32)
        token_exp_timestamp = str(
            get_current_time_milli_sec() + TOKEN_EXP_TIME_GAP * 1000)
        next_token_request_timestamp = str(
            get_current_time_milli_sec() + TOKEN_ATTEMPT_TIME_GAP * 1000)
        if token_request_count >= MAXIMUM_TOKEN_REQUEST_COUNT:
            token_request_count = 1
        else:
            token_request_count += 1
        is_token_add_or_updated = update_token_data_by_user_ag_id(
            user_ag_id, token, token_exp_timestamp,
            token_request_count, next_token_request_timestamp)

    if not is_token_add_or_updated:
        return get_response(False,
                            UserMessages.PLEASE_VERIFY_MAIL,
                            {}), 400
    verification_link = f"{BASE_URL}/email-verify/{token}"
    email_body = f"Click the link to verify your email: {verification_link}"

    is_email_sent = send_email('Resend Email Verification', email,
                               email_body)
    if not is_email_sent:
        return get_response(False,
                            UserMessages.PLEASE_VERIFY_MAIL,
                            {}), 400

    return get_response(True, UserMessages.SUCCESS_VERIFY_MAIL_RESEND,
                        {"home_page_redirection": False}), 200
