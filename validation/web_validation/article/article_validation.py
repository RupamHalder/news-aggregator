from app_session.user_session import get_logged_in_user_id
from constants.messages import UserMessages, CommonMessages
from model.user.user import is_username_exist
from utils.utility import get_response, is_email_valid, \
    check_password_validity, is_param_empty


def save_article_field_validation(request):
    data = request.get_json()
    user_id = get_logged_in_user_id()
    title = data.get('title', '').strip()
    url = data.get('url', '').strip()
    description = data.get('description', '').strip()
    article_image_url = data.get('article_image_url', '').strip()
    sentiment = data.get('sentiment', '').strip()

    # if is_param_empty(email) or is_param_empty(password):
    #     return get_response(False, UserMessages.REQUIRE_EMAIL_PASS, {}), 400
    #
    # if not is_email_valid(email):
    #     return get_response(False, UserMessages.INVALID_EMAIL, {}), 400
    #
    # if is_username_exist(email):
    #     return get_response(False, UserMessages.EXISTS_EMAIL, {}), 400


    return get_response(True, CommonMessages.SUCCESS, {
        "user_id": user_id,
        "title": title,
        "url": url,
        "description": description,
        "article_image_url": article_image_url,
        "sentiment": sentiment
    }), 200
