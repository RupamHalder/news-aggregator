class CommonMessages:
    SUCCESS = '''Success.'''

    FAIL_SOMETHING_WENT_WRONG = '''Something went wrong. Please try again later.'''


class UserMessages:
    ALREADY_MAIL_VERIFIED = '''Your email is already verified please login.'''

    REQUIRE_EMAIL_PASS = '''Email and password are required.'''
    REQUIRE_DIGIT_IN_PASS = '''Password must contain at least one digit.'''
    REQUIRE_UPPER_IN_PASS = '''Password must contain at least one uppercase letter.'''
    REQUIRE_LOWER_IN_PASS = '''Password must contain at least one lowercase letter.'''
    REQUIRE_SPECIAL_IN_PASS = '''Password must contain at least one special character.'''

    INVALID_EMAIL = '''Invalid email address.'''
    INVALID_PASS_LENGTH = '''Password must be at least 8 characters long.'''
    INVALID_EMAIL_VERIFY_TOKEN = ''''Invalid email verify token.'''

    EXPIRED_EMAIL_VERIFY_TOKEN = ''''The verification link has expired.'''

    EXISTS_EMAIL = '''An user with this email is already registered.'''

    NOT_EXISTS_EMAIL = '''This email doesn't match our records.'''

    PLEASE_LOGIN = '''Please login first.'''
    PLEASE_VERIFY_MAIL = '''Please verify your email before login.'''

    UNMATCHED_CONF_PASS = '''Password and confirm password must match'''

    SUCCESS_PASS_VALID = '''Password is valid.'''
    SUCCESS_USER_REGISTRATION = '''User registered successfully. Verification email sent.'''
    SUCCESS_USER_LOGIN = '''You are successfully logged in.'''
    SUCCESS_USER_LOGOUT = '''You are successfully logged out.'''
    SUCCESS_VERIFY_MAIL_RESEND = '''Please verify your email before login using the link sent to your email.'''
    SUCCESS_VERIFY_MAIL = '''Email verified successfully.'''

    FAIL_USER_REGISTRATION = '''User registration failed.'''
    FAIL_USER_LOGIN = '''Incorrect email or password.'''
    FAIL_VERIFY_MAIL_SEND = '''Unable to send verification email.'''
    FAIL_VERIFY_MAIL_RESEND = '''Unable to resend verification email.'''
    FAIL_VERIFY_MAIL_TOKEN_GEN = '''Cannot request a new token yet. Try later.'''
    FAIL_VERIFY_MAIL = '''Unable to verify email.'''
