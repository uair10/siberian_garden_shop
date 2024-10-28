from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Настройки из .env файла"""

    FLASK_APP = environ.get("FLASK_APP")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Flask-SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    FLASK_ADMIN_SWATCH = "cerulean"
    SESSION_COOKIE_SAMESITE = "Lax"

    # Flask Babel
    LANGUAGES = ["ru", "en"]

    FILEUPLOAD_IMG_FOLDER = path.join(basedir, "uploads")
    FILEUPLOAD_ALLOWED_EXTENSIONS = ["xlsx"]


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    SQLALCHEMY_ECHO = True
    TESTING = True
