import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.environ['DATABASE_URL'], convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Accesses(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    article = Column(String(60), unique=True)
    access_key = Column(String(37))

    def __init__(self, article=None, access_key=None):
        self.article = article
        self.access_key = access_key

    def __repr__(self):
        return '<Article {}>'.format(self.article)


Base.metadata.create_all(bind=engine)


def get_access_key(article_title):
    article = Accesses.query.filter(Accesses.article == article_title).first()
    return article.access_key
