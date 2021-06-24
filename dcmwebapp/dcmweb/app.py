###############################################
# Universidade Federal do Rio de Janeiro
# Engenharia Eletrônica e da Computação
# DCM - Data Center Manager
# Aluno: Ewerton Vasconcelos da Silva
# Orientador: Rodrigo de Souza Couto 
###############################################
#Credits to: 


from flask import Flask
from flask_oidc import OpenIDConnect
from config import config
from backend.utils import configure_logger


app = None
oidc = OpenIDConnect()
_logger = None


def create_app():
    global app, oidc, _logger, db
    app = Flask(__name__)

    # Load the configurations based on the 'FLASK_ENV' environment variable
    app.config.from_object(config)
    
    # Initialize logger
    _logger = configure_logger(app)
    # Init the OpenIDConnect application instance
    oidc.init_app(app)

    from backend.views import view as view_blueprint
    app.register_blueprint(view_blueprint)

    return app
