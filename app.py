from flask import Flask
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_cors import CORS

from conf_enviroment.conf_env import config
from controller.web_controller.article.article_api_controller import \
    article_api_controller
from controller.web_controller.page_controller import page_controller
from controller.web_controller.user.user_controller import user_controller
from controller.web_controller.article.article_controller import \
    article_controller
from utils.utility import get_response

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
csrf = CSRFProtect(app)
CORS(app, origins=[])

app.register_blueprint(page_controller)
app.register_blueprint(user_controller, url_prefix='/api/v1/user')
app.register_blueprint(article_controller, url_prefix='/api/v1/article')
app.register_blueprint(article_api_controller, url_prefix='/api/v1/article_api')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    print("CSRF Error: " + e.description)
    # Possible "description" values:
    # The CSRF token is missing.
    # The CSRF token has expired.
    return get_response(False, "Please refresh the page and try again.",
                        {}), 403


if __name__ == '__main__':
    # '0.0.0.0' = 127.0.0.1 i.e. localhost
    # port = 5000 : we can modify it for localhost
    app.run(host='0.0.0.0', port=5000)  # local webserver : app.run()
