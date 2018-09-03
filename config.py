import os
import dropbox

basedir = os.path.abspath(os.path.dirname(__file__))
bd_url = 'postgres://foozxnzwuiiwzj:28e7a30f20ec57c5ac55629cac296d00e6b87c230f76cf7a437a9186d6aabb3e@ec2-54-247-101-202.eu-west-1.compute.amazonaws.com:5432/d5gn733ism5h42'


def get_article_path(article_url, app_dir=basedir):
    article_path = os.path.join(
        app_dir,
        'articles',
        '{}.html'.format(article_url)
    )
    return article_path


def get_article_txt_path(article_url, app_dir=basedir):
    article_path = os.path.join(
        app_dir,
        'articles',
        '{}.txt'.format(article_url)
    )
    return article_path


def has_file(article_url):
    if os.path.exists(get_article_path(article_url)):
        return True
    dbx = dropbox.Dropbox("s4KdX67CS1AAAAAAAAAAFqAJ7F1_vsufKA2gbd8y_TQHGBv15DiQeokOLDoCKXZz")
    try:
        dbx.files_download_to_file(get_article_path(article_url), '/{}.html'.format(article_url))
    except dropbox.exceptions.ApiError:
        return False
    return True


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']
    WTF_CSRF_SECRET_KEY = os.environ['CSRF_SECRET_KEY']
    TEMPLATES_AUTO_RELOAD = True
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True


class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:///accesses.db'
    DEBUG = True
