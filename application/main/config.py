import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    MAIN_PATH = basedir
    UPLOAD_FOLDER = './resources/uploads'
    ORIGINAL_FILE_FOLDER = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
        0]+'\\resources\\uploads'
    RESULT_FOLDER = './resources/classified/result'
    UPLOAD_WIKIEDIT_REQUEST_FOLDER = './resources/classified/requested'
    UPLOAD_COMPLETED_FOLDER = './resources/classified/completed'

    # PYWIKICONFIGURATION
    PYWIKI_FAMILY_FILE = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
        0]+'\\config\\my_family.py'
    PYWIKI_USER_PASSWORD_FILE = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
        0]+'\\user-password.py'
    WIKI_USER_NAME = 'WikibaseAdmin'
    WIKI_BOT_USER_NAME = 'bot_user_1'
    WIKI_BOT_SECRET = 'cicb8eb65ktd956a0b43vauc4o63fpak'
    WIKI_SPARQL_END_POINT = 'http://localhost:8989/bigdata/namespace/wdq/sparql'
    WIKI_DOMAIN = 'localhost:8181'
    WIKI_PROTOCOL = 'http'
    WIKI_API_URI = 'http://localhost:8181/w/api.php'


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    #     os.path.join(basedir, 'flask_boilerplate_main.db')
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{server}/dis_wiki".format(
    #     username='root', password='password', server='MariaDB')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@127.0.0.1/dis_wiki"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    #     os.path.join(basedir, 'flask_boilerplate_test.db')

    # SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{server}/testdb".format(
    #     username, password, server)

    # SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{server}/testdb".format(
    #     username='root', password='password', server='MariaDB')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@127.0.0.1/dis_wiki_test"

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
