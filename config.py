import os

basedir = os.path.abspath(os.path.dirname(__file__))


def get_article_path(article_url, app_dir=basedir):
    article_path = os.path.join(
        app_dir,
        'articles',
        '{}.html'.format(article_url)
    )
    return article_path


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = ['SECRET_KEY']
    WTF_CSRF_SECRET_KEY = ['CSRF_SECRET_KEY']
    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_SECURE = True
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True


class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:///accesses.db'
    DEBUG = True
