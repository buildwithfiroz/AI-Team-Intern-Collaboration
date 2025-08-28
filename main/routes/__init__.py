from .home import home_bp
from .login import login_bp
from .logout import logout_bp
from .signup import signup_bp
from .dashboard import dashboard_bp
from .input_url import input_url_bp
from .chat import chat_bp

all_blueprints = [
    login_bp,
    logout_bp,
    signup_bp,
    dashboard_bp,
    input_url_bp,
    chat_bp,
    home_bp
]
