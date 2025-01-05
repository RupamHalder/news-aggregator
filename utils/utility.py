import re
import time
import uuid
import hashlib

from constants.messages import UserMessages


def get_current_time_milli_sec():
    return round(time.time() * 1000)


# Format in 13/11/2024 10:43 pm
def datetime_to_string(dt):
    try:
        return dt.strftime("%d/%m/%Y %I:%M %p")
    except:
        return ""


def generate_auto_id(prefix, length=16):
    id = str(get_current_time_milli_sec()) + str(uuid.uuid4())[
                                             :length].replace("-", "")
    # id = prefix + "_" + str(id)[:length]
    id = prefix + "_" + str(id)[:length]
    return id


def generate_token(length=16):
    token = str(get_current_time_milli_sec()) + str(uuid.uuid4())[
                                                :length].replace("-", "")
    return token


def encryption_sha_256(string):
    result = hashlib.sha256(string.encode())
    return result.hexdigest()


def get_response(status, message, data):
    return {
        "status": status,
        "message": message,
        "data": data
    }


def is_email_valid(email):
    try:
        if email is not None:
            regex_email = re.compile(
                '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            email_object = regex_email.match(email)
        else:
            email_object = None
        if email_object is not None:
            return True
        else:
            return False
    except:
        return False


def check_password_validity(password):
    if len(password) < 8:
        return False, UserMessages.INVALID_PASS_LENGTH
    elif not any(char.isdigit() for char in password):
        return False, UserMessages.REQUIRE_DIGIT_IN_PASS
    elif not any(char.isupper() for char in password):
        return False, UserMessages.REQUIRE_UPPER_IN_PASS
    elif not any(char.islower() for char in password):
        return False, UserMessages.REQUIRE_LOWER_IN_PASS
    elif not any(char in "`~!@#$%^&*()-+_={}[]|\\:;\"'<>?,./" for char in password):
        return False, UserMessages.REQUIRE_SPECIAL_IN_PASS
    else:
        return True, UserMessages.SUCCESS_PASS_VALID


def is_param_empty(param):
    if param is None or param == "":
        return True
    else:
        return False
