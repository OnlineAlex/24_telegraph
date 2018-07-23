import datetime
import re
import uuid
from transliterate import translit
from bs4 import BeautifulSoup
from html2text import HTML2Text
from flask import render_template
from config import get_article_path
from db import db_session, Accesses


class Article:
    def __init__(self, title, author, text):
        self.title = title
        self.author = author
        self.text = text
        self.url = self.get_friendly_url()
        self.access_key = self.create_access_key()

    def get_friendly_url(self):
        today = datetime.datetime.now().strftime('%d-%m-%Y')
        translit_title = translit(self.title, 'ru', reversed=True)
        url_words = re.split('\W+', translit_title)
        url_text = '-'.join(url_words[:5])[:40].rstrip('-')
        url = '{}-{}'.format(translit(url_text.lower(), 'ru', reversed=True,), today)
        return '{}-{}'.format(url, uuid.uuid4().hex[:5])

    @staticmethod
    def create_access_key():
        return str(uuid.uuid4())

    def render_article_block(self):
        return render_template(
            'article-block.html',
            title=self.title,
            author=self.author,
            text=self.text
        )

    @staticmethod
    def add_article_page(article_page, url):
        article_path = get_article_path(url)
        with open(article_path, 'w+') as new_article:
            new_article.write(article_page)

    def add_article_to_db(self):
        article = Accesses(self.url, self.access_key)
        db_session.add(article)
        db_session.commit()


class ArticleBlock:
    def __init__(self, html_content):
        self.article_page = self._get_bs_object(html_content)

    @staticmethod
    def _get_bs_object(page):
        return BeautifulSoup(page, 'html.parser')

    def get_title(self):
        return self.article_page.select_one('#title').text

    def get_author(self):
        author = self.article_page.select_one('#author')
        if author is None:
            return False
        return author.text

    def get_text(self):
        return self.article_page.select_one('#text')

    def get_markdown_content(self):
        html_content = self.get_text()
        text_maker = HTML2Text()
        text_maker.body_width = 0
        text_maker.single_line_break = True
        return text_maker.handle(str(html_content))
