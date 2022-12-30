from logging.config import dictConfig
from flask import Flask
from config import LocalConfig, TestConfig
from app.controllers.rates import rates_api
from app.extensions import db


def create_app(config: object = None) -> Flask:
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )

    app: Flask = Flask(__name__)

    if config == "test":
        app.config.from_object(TestConfig())
    elif config == "local":
        app.config.from_object(LocalConfig())
    elif config is None:
        # load the local config if no config is passed
        app.config.from_object(LocalConfig())
    else:
        # load the config if passed in
        app.config.from_object(config)

    db.init_app(app)
    app.register_blueprint(rates_api)

    @app.route("/")
    def hello():
        return "Hello"

    return app
