import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine(os.environ['DATABASE_URL'], convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Accesses(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    url = Column(String(100), unique=True)
    file = Column(String, unique=True)
    title = Column(String)
    plan = Column(String)
    text = Column(String)

    def __init__(self, url=None, file=None, title=None, plan= None, text=None):
        self.url = url
        self.file = file
        self.title = title
        self.plan = plan
        self.text = text


    def __repr__(self):
        return '<Article {}>'.format(self.url)


Base.metadata.create_all(bind=engine)

def is_new(article_url):
    article = Accesses.query.filter(Accesses.url == article_url).first()
    return not bool(article)


def update_article(article_url, title, plan, text):
    article = Accesses.query.filter(Accesses.url == article_url).first()
    article.title = title
    article.plan = plan
    article.text = text

def get_article(article_url):
    article = Accesses.query.filter(Accesses.url == article_url).first()
    return article
