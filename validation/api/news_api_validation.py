from constants.messages import CommonMessages
from utils.utility import get_response, convert_str_to_int


def get_articles_field_validation(request):
    data = request.get_json()
    sources = data.get('sources', []).strip()

    return get_response(True, CommonMessages.SUCCESS, {
        "sources": sources
    }), 200

def get_news_sources_field_validation(request):
    data = request.args
    page = data.get('page', 1)

    return get_response(True, CommonMessages.SUCCESS, {
        "page": convert_str_to_int(page)
    }), 200
