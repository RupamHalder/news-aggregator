from flask import jsonify

from flask import Blueprint, render_template, request

from model.user.user import add_user, is_username_exist, update_is_verified, \
    is_email_verified
from model.user.user_email_verify_token import add_email_verify_token, \
    get_token_data_by_token, update_token_data_object, get_token_data_by_email
from service.others.mail import send_email
from utils.utility import is_email_valid, get_current_time_milli_sec, \
    generate_token, generate_auto_id, check_password_validity

user_controller = Blueprint('user_controller', __name__)

BASE_URL = "http://localhost:5001/"


# Routes
@user_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    if not is_email_valid(email):
        return jsonify({'message': 'Invalid email address.'}), 400

    if is_username_exist(email):
        return jsonify({'message': 'Email already exists.'}), 400

    is_password_valid, message = check_password_validity(password)
    if not is_password_valid:
        return jsonify({'message': message}), 400

    user_ag_id = generate_auto_id(prefix="user", length=32)
    is_user_added = add_user(user_ag_id=user_ag_id, username=email,
                             password=password)

    if not is_user_added:
        return jsonify({'message': 'User registration failed.'}), 500

    token = generate_token(32)
    token_exp_timestamp = str(
        get_current_time_milli_sec() + 15 * 60 * 1000)
    token_request_count = 1
    next_token_request_timestamp = str(
        get_current_time_milli_sec() + 5 * 60 * 1000)

    is_token_added = add_email_verify_token(user_ag_id, token,
                                            token_exp_timestamp,
                                            token_request_count,
                                            next_token_request_timestamp)

    if not is_token_added:
        return jsonify({'message': 'User registration failed.'}), 500

    verification_link = f"{BASE_URL}/email-verify/{token}"
    email_body = f"Click the link to verify your email: {verification_link}"

    is_email_sent = send_email('Verify Your Email', email, email_body)

    if not is_email_sent:
        return jsonify({'message': 'Unable to send verification email.'}), 500

    return jsonify({
        'message': 'User registered successfully. Verification email sent.'}), 200


@user_controller.route('/email-verify/<token>', methods=['GET'])
def verify_email(token):
    token_data = get_token_data_by_token(token)

    if not token_data:
        return jsonify({'message': 'Invalid token.'}), 400

    if get_current_time_milli_sec() > int(token_data.token_exp_timestamp):
        return jsonify({'message': 'Token has expired.'}), 400

    token_data.token_exp_timestamp = str(
        int(token_data.token_exp_timestamp) + 15 * 60 * 1000
    )
    token_data.token_request_count = 0

    is_token_updated = update_token_data_object(token_data)
    if not is_token_updated:
        return jsonify({'message': 'Unable to verify email.'}), 400

    is_verified_updated = update_is_verified(token_data.user_ag_id, True)

    if not is_verified_updated:
        return jsonify({'message': 'Unable to verify email.'}), 400

    return jsonify({'message': 'Email verified successfully.'}), 200


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
    ) and token_data.token_request_count >= 3:
        return jsonify(
            {'message': 'Cannot request a new token yet. Try later.'}), 400

    token = generate_token()
    token_data.token = token
    token_data.token_exp_timestamp = str(
        get_current_time_milli_sec() + 15 * 60 * 1000)
    token_data.next_token_request_timestamp = str(
        get_current_time_milli_sec() + 5 * 60 * 1000)
    if token_data.token_request_count >= 3:
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
