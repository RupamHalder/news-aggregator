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


def destroy_user_session():
    try:
        session['user_data'] = None
        session['is_active'] = False
        return True
    except:
        print("Error in destroy_user_session function:")
        print(traceback.format_exc())
        return False


# Decorator for checking if user is logged in before
# for accessing specific resource i.e. page or api
def is_user_logged_in(resource_type):
    def decorator_wrapper(f):
        def wrapper(*args, **kwargs):
            print(session.get('is_active'))
            if session.get('is_active') is True:
                return f(*args, **kwargs)
            else:
                if resource_type == "page":
                    flash(UserMessages.PLEASE_LOGIN, 'error')
                    return redirect(url_for('page_controller.login_page'))
                else: # api
                    return get_response(False, UserMessages.PLEASE_LOGIN,
                                        {}), 401

        return wrapper

    return decorator_wrapper
