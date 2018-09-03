import datetime
import re
import uuid
import dropbox
from transliterate import translit
from flask import render_template
from config import get_article_path
from db import db_session, Accesses, is_new, update_article


class Article:
    def __init__(self, title, plan, plan_html, text, text_html):
        self.title = title
        self.plan = plan
        self.plan_html = plan_html
        self.text = text
        self.text_html = text_html
        self.url = self.get_friendly_url()
        self.file = None

    def get_friendly_url(self):
        translit_title = translit(self.title, 'ru', reversed=True)
        url_words = re.split('\W+', translit_title)
        url_text = '-'.join(url_words).rstrip('-')
        url = '{}-{}'.format(translit(url_text.lower(), 'ru', reversed=True,), uuid.uuid4().hex[:5])
        return url

    @staticmethod
    def create_access_key():
        return str(uuid.uuid4())

    def render_article_block(self):
        return render_template(
            'article-block.html',
            title=self.title,
            plan=self.plan_html,
            text=self.text_html
        )

    def add_article_page(self, article_page, url):
        article_path = get_article_path(url)
        dbx = dropbox.Dropbox("s4KdX67CS1AAAAAAAAAAFqAJ7F1_vsufKA2gbd8y_TQHGBv15DiQeokOLDoCKXZz")
        with open(article_path, 'w+') as new_article:
            new_article.write(article_page)
        with open(article_path, 'rb') as new_article:
            dbx.files_upload(new_article.read(), '/{}.html'.format(self.url), mode=dropbox.files.WriteMode("overwrite"))

    def add_article_to_db(self):
        if is_new(self.url):
            article = Accesses(self.url, self.file, self.title, self.plan, self.text)
            db_session.add(article)
        else:
            article = Accesses.query.filter(Accesses.url == self.url).first()
            article.title = self.title
            article.plan = self.plan
            article.text = self.text
        db_session.commit()
