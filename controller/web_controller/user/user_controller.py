import traceback

from flask import jsonify

from flask import Blueprint, render_template, request

from model.user.user import add_user, is_username_exist, is_email_verified
from model.user.user_email_verify_token import add_email_verify_token, \
    update_token_data_object, get_token_data_by_email
from service.others.mail import send_email
from service.web_service.user.user_service import login_service, register_service
from utils.utility import is_email_valid, get_current_time_milli_sec, \
    generate_token, generate_auto_id, check_password_validity, get_response
from constants.messages import UserMessages, CommonMessages
from validation.web_validation.user.user_validation import \
    register_field_validation, login_field_validation

user_controller = Blueprint('user_controller', __name__)

BASE_URL = "http://localhost:5001/"
TOKEN_EXP_TIME_GAP = 15 * 60
TOKEN_ATTEMPT_TIME_GAP = 5 * 60
MAXIMUM_TOKEN_REQUEST_COUNT = 3


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


@user_controller.route('/resend-verification', methods=['POST'])
def resend_verification():
    data = request.get_json()
    email = data.get('email')

    if not is_username_exist(email):
        return jsonify({'message': 'This email is not registered.'}), 404

    if is_email_verified(email):
        return jsonify({'message': 'Email is already verified.'}), 400

    token_data = get_token_data_by_email(email)
    if not token_data:
        return jsonify({'message': 'Token not found.'}), 404

    if get_current_time_milli_sec() < int(
            token_data.next_token_request_timestamp
    ) and token_data.token_request_count >= MAXIMUM_TOKEN_REQUEST_COUNT:
        return jsonify(
            {'message': 'Cannot request a new token yet. Try later.'}), 400

    token = generate_token()
    token_data.token = token
    token_data.token_exp_timestamp = str(
        get_current_time_milli_sec() + TOKEN_EXP_TIME_GAP * 1000)
    token_data.next_token_request_timestamp = str(
        get_current_time_milli_sec() + TOKEN_ATTEMPT_TIME_GAP * 1000)
    if token_data.token_request_count >= MAXIMUM_TOKEN_REQUEST_COUNT:
        token_data.token_request_count = 1
    else:
        token_data.token_request_count += 1

    is_token_updated = update_token_data_object(token_data)
    if not is_token_updated:
        return jsonify(
            {'message': 'Unable to resend verification email.'}), 400
    verification_link = f"{BASE_URL}/email-verify/{token}"
    email_body = f"Click the link to verify your email: {verification_link}"

    is_email_sent = send_email('Resend Email Verification', email, email_body)
    if not is_email_sent:
        return jsonify(
            {'message': 'Unable to resend verification email.'}), 400

    return jsonify({'message': 'Verification email resent.'}), 200


@user_controller.route('/email-verify-page/<token>', methods=['GET'])
def email_verify_page(token):
    return render_template('email_verify.html', token=token)
