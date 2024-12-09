from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect, CSRFError

from conf_enviroment.conf_env import config
from controller.web_controller.page_controller import page_controller
from utils.utility import get_response

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
csrf = CSRFProtect(app)

app.register_blueprint(page_controller)


@app.route('/')
def index():
    # Home page content
    return redirect(url_for('page_controller.dashboard'))


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
    app.run(host='0.0.0.0', port=5000,
            debug=True)  # local webserver : app.run()
