from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve
import db_operations


app = Flask(__name__)
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app)


def create_app():
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db_operations.get_user_by_id(user_id)

    from main import main
    app.register_blueprint(main)

    from auth import auth
    app.register_blueprint(auth)

    return serve(app, host="0.0.0.0", port=5000, threads=4)


if __name__ == '__main__':
    create_app()
