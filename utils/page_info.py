from conf_enviroment.conf_env import config


def get_page_info(page_name):
    # Before Login
    if page_name == 'index':
        return home_page_info()
    if page_name == 'login':
        return login_page_info()
    if page_name == 'register':
        return register_page_info()
    
    # After Login
    if page_name == 'saved-articles':
        return saved_articles_page_info()
    else:
        return page_not_found_info()


def page_not_found_info():
    return {
        'app_name': config.APP_NAME or '',
        'page_heading': 'Page Not Found',
        'title': (config.APP_NAME or '') + (
            ' - ' if config.APP_NAME else '') + 'Page Not Found',
        'description': 'Page Not Found',
        'keywords': 'Page Not Found'
    }


def home_page_info():
    return {
        'app_name': config.APP_NAME or '',
        'page_heading': 'Latest News Articles',
        'title': (config.APP_NAME or '') + (
            ' - ' if config.APP_NAME else '') + 'Home',
        'description': 'News Aggregator Home Page',
        'keywords': 'News Aggregator'
    }


def login_page_info():
    return {
        'app_name': config.APP_NAME or '',
        'page_heading': 'Login',
        'title': f"{config.APP_NAME} - Login" if config.APP_NAME else 'Login',
        'description': 'Login Page',
        'keywords': 'News Aggregator Login'
    }


def register_page_info():
    return {
        'app_name': config.APP_NAME or '',
        'page_heading': 'Register',
        'title': f"{config.APP_NAME} - Register" if config.APP_NAME else 'Register',
        'description': 'Registration Page',
        'keywords': 'News Aggregator Register'
    }


def saved_articles_page_info():
    return {
        'app_name': config.APP_NAME or '',
        'page_heading': 'Saved Articles',
        'title': (config.APP_NAME or '') + (
            ' - ' if config.APP_NAME else '') + 'Home',
        'description': 'News Aggregator Saved Articles Page',
        'keywords': 'News Aggregator'
    }
