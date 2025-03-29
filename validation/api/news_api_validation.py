from constants.messages import CommonMessages
from utils.utility import convert_empty_str_to_none, get_response, convert_str_to_int, is_param_empty


def get_articles_field_validation(request):
    data = request.get_json()
    sources = data.get('sources', [])
    news_query = data.get('news_query', '').strip()
    language = data.get('language', '').strip()
    country = data.get('country', '').strip()
    category = data.get('category', '').strip()
    page_size = data.get('page_size', 10)
    page = data.get('page', 1)

    return get_response(True, CommonMessages.SUCCESS, {
        "sources": sources,
        "news_query": news_query,
        "language": language,
        "country": country,
        "category": category,
        "page_size": convert_str_to_int(page_size),
        "page": convert_str_to_int(page)
    }), 200


def get_news_sources_field_validation(request):
    data = request.args
    language = data.get('language', None)
    country = data.get('country', None)
    category = data.get('category', None)
    q = data.get('q', '').strip()
    page = data.get('page', 1)

    return get_response(True, CommonMessages.SUCCESS, {
        "page": convert_str_to_int(page),
        "q": q,
        "language": language,
        "country": country,
        "category": category
    }), 200


def get_country_lang_category_field_validation(request):
    data = request.args
    q = data.get('q', '').strip()
    page = data.get('page', 1)
    resource_type = data.get('resource_type', '')

    if is_param_empty(resource_type):
        get_response(False, 'Resource type is missing.', {}), 400
    
    if resource_type not in {"country", "language", "category"}:
        get_response(False, 'Invalid resource type!', {}), 400

    return get_response(True, CommonMessages.SUCCESS, {
        "page": convert_str_to_int(page),
        "q": q,
        "resource_type": resource_type,
    }), 200
