class CommonMessages:
    SUCCESS = '''Success.'''

    FAIL_SOMETHING_WENT_WRONG = '''Something went wrong. Please try again later.'''

class UserMessages:
    REQUIRE_EMAIL_PASS = '''Email and password are required.'''
    REQUIRE_DIGIT_IN_PASS = '''Password must contain at least one digit.'''
    REQUIRE_UPPER_IN_PASS = '''Password must contain at least one uppercase letter.'''
    REQUIRE_LOWER_IN_PASS = '''Password must contain at least one lowercase letter.'''
    REQUIRE_SPECIAL_IN_PASS = '''Password must contain at least one special character.'''
    
    INVALID_EMAIL = '''Invalid email address.'''
    INVALID_PASS_LENGTH = '''Password must be at least 8 characters long.'''
    
    EXISTS_EMAIL = '''Email already exists.'''

    NOT_EXISTS_EMAIL = '''This email doesn't match our records.'''

    PLEASE_LOGIN = '''Please login first.'''

    SUCCESS_PASS_VALID = '''Password is valid.'''
    SUCCESS_USER_REGISTRATION = '''User registered successfully. Verification email sent.'''

    FAIL_USER_REGISTRATION = '''User registration failed.'''
    FAIL_VERIFY_MAIL_SEND = '''Unable to send verification email.'''
