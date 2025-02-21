from app_session.user_session import get_logged_in_user_id
from constants.messages import ArticleMessages, CommonMessages
from model.article.article_saved import is_article_table_field_exist
from model.user.user import is_user_id_exist
from utils.utility import get_response, is_param_empty, is_str_float


def save_article_field_validation(request):
    data = request.get_json()
    user_id = get_logged_in_user_id()
    title = data.get('title', '').strip()
    url = data.get('url', '').strip()
    description = data.get('description', '').strip()
    article_image_url = data.get('article_image_url', '').strip()
    sentiment = data.get('sentiment', None)
    published_at = data.get('published_at', '')

    if is_param_empty(user_id):
        return get_response(False, ArticleMessages.MISSING_USER_ID, {}), 404
    
    if is_param_empty(title):
        return get_response(False, ArticleMessages.MISSING_TITLE, {}), 404
    
    if is_param_empty(url):
        return get_response(False, ArticleMessages.MISSING_URL, {}), 404
    
    if is_param_empty(sentiment):
        return get_response(False, ArticleMessages.MISSING_SENTIMENT, {}), 404
    
    if not is_str_float(sentiment):
        return get_response(False, ArticleMessages.INVALID_SENTIMENT, {}), 400
    
    if not is_user_id_exist(user_id):
        return get_response(False, ArticleMessages.INVALID_USER_ID, {}), 400
    
    if is_article_table_field_exist([url], ['url']):
        return get_response(False, ArticleMessages.EXISTS_ARTICLE, {}), 400

    return get_response(True, CommonMessages.SUCCESS, {
        "user_id": user_id,
        "title": title,
        "url": url,
        "description": description,
        "article_image_url": article_image_url,
        "sentiment": sentiment,
        "published_at": published_at
    }), 200


def delete_article_field_validation(request):
    data = request.get_json()
    user_id = get_logged_in_user_id()
    saved_article_id = data.get('saved_article_id', '').strip()

    if is_param_empty(user_id):
        return get_response(False, ArticleMessages.MISSING_USER_ID, {}), 404
    
    if is_param_empty(saved_article_id):
        return get_response(False, ArticleMessages.MISSING_ARTICLE_ID, {}), 404
    
    if not is_user_id_exist(user_id):
        return get_response(False, ArticleMessages.INVALID_USER_ID, {}), 400
    
    if not is_article_table_field_exist([saved_article_id], ['saved_article_ag_id']):
        return get_response(False, ArticleMessages.INVALID_ARTICLE_ID, {}), 400
    
    if not is_article_table_field_exist([user_id, saved_article_id], ['user_id', 'saved_article_ag_id']):
        return get_response(False, ArticleMessages.DOES_NOT_BELONG_TO_USER, {}), 400

    return get_response(True, CommonMessages.SUCCESS, {
        "saved_article_id": saved_article_id
    }), 200
