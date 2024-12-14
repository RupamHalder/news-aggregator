import uuid
import time
import smtplib
from email.mime.text import MIMEText

from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from flask import Blueprint, render_template, request

from utils.utility import is_email_valid, get_current_time_milli_sec, \
    generate_token

user_controller = Blueprint('user_controller', __name__)

# SMTP configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@example.com'
SMTP_PASSWORD = 'your-password'


def send_email(subject, recipient, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, recipient, msg.as_string())


# Routes

@user_controller.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    if not is_email_valid(email):
        return jsonify({'message': 'Invalid email address.'}), 400

    try:
        user = User(user_ag_id=generate_token(32), username=email,
                    password=password)
        session.add(user)
        session.commit()

        token = generate_token()
        token_data = EmailVerifyToken(
            user_ag_id=user.user_ag_id,
            token=token,
            token_exp_timestamp=str(get_current_time_milli_sec() + 15 * 60 * 1000),
            token_request_count=1,
            next_token_request_timestamp=str(get_current_time_milli_sec() + 5 * 60 * 1000)
        )

        session.add(token_data)
        session.commit()

        verification_link = f"http://localhost:5000/email-verify/{token}"
        email_body = f"Click the link to verify your email: {verification_link}"

        send_email('Verify Your Email', email, email_body)

        return jsonify({
                           'message': 'User registered successfully. Verification email sent.'}), 201
    except exc.IntegrityError:
        session.rollback()
        return jsonify({'message': 'Email is already registered.'}), 400


@user_controller.route('/email-verify/<token>', methods=['GET'])
def verify_email(token):
    token_data = session.query(EmailVerifyToken).filter_by(token=token).first()

    if not token_data:
        return jsonify({'message': 'Invalid token.'}), 400

    if get_current_time_milli_sec() > int(token_data.token_exp_timestamp):
        return jsonify({'message': 'Token has expired.'}), 400

    user = session.query(User).filter_by(
        user_ag_id=token_data.user_ag_id).first()
    if user:
        user.status = True
        session.commit()
        return jsonify({'message': 'Email verified successfully.'}), 200

    return jsonify({'message': 'User not found.'}), 404


@user_controller.route('/resend-verification', methods=['POST'])
def resend_verification():
    data = request.json
    email = data.get('email')

    user = session.query(User).filter_by(username=email).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    if user.status:
        return jsonify({'message': 'User is already verified.'}), 400

    token_data = session.query(EmailVerifyToken).filter_by(
        user_ag_id=user.user_ag_id).first()
    if not token_data:
        return jsonify({'message': 'Token not found.'}), 404

    if get_current_time_milli_sec() < int(token_data.next_token_request_timestamp):
        return jsonify(
            {'message': 'Cannot request a new token yet. Try later.'}), 400

    token = generate_token()
    token_data.token = token
    token_data.token_exp_timestamp = str(get_current_time_milli_sec() + 15 * 60 * 1000)
    token_data.next_token_request_timestamp = str(
        get_current_time_milli_sec() + 5 * 60 * 1000)
    token_data.token_request_count += 1
    session.commit()

    verification_link = f"http://localhost:5000/email-verify/{token}"
    email_body = f"Click the link to verify your email: {verification_link}"

    send_email('Resend Email Verification', email, email_body)

    return jsonify({'message': 'Verification email resent.'}), 200


@user_controller.route('/email-verify-page/<token>', methods=['GET'])
def email_verify_page(token):
    return render_template('email_verify.html', token=token)
