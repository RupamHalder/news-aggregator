import traceback

from flask import session, redirect, url_for, flash

from constants.messages import UserMessages
from utils.utility import get_response


def create_user_session(user_data):
    try:
        session['user_data'] = user_data
        session['is_active'] = True
        return True
    except:
        print("Error in create_user_session function:")
        print(traceback.format_exc())
        return False


# Decorator for checking if user is logged in
def is_user_logged_in(resource_type="page"):
    def decorator_wrapper(f):
        def wrapper(*args, **kwargs):
            print(session.get('is_active'))
            if session.get('is_active') is True:
                return f(*args, **kwargs)
            else:
                if resource_type == "page":
                    flash(UserMessages.PLEASE_LOGIN, 'danger')
                    return redirect(url_for('page_controller.login_page'))
                else: # api
                    return get_response(False, UserMessages.PLEASE_LOGIN,
                                        {}), 401

        return wrapper

    return decorator_wrapper
