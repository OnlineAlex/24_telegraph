import os
from flask import Flask, render_template, request, redirect, make_response
from flask_simplemde import SimpleMDE
from flask_wtf import CSRFProtect
from flask_sslify import SSLify


import config
import db
from models import Article, ArticleBlock


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(config.Config)
SimpleMDE(app)
sslify = SSLify(app)

try:
    os.mkdir(os.path.join(config.basedir, 'articles'))
except OSError:
    pass


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        form_data = dict(request.form)
        article = Article(
            form_data['title'][0],
            form_data['signature'][0],
            form_data['article'][0]
        )
        article_block = article.render_article_block()
        article.add_article_page(article_block, article.url)
        response = make_response(redirect(article.url))
        if 'access' not in request.cookies:
            year = 60*60*24*365
            response.set_cookie('access', str(article.access_key), max_age=year)
        else:
            article.access_key = request.cookies.get('access')
        article.add_article_to_db()
        return response

    return render_template('form.html')


@app.route('/<article_url>', methods=['GET'])
def content(article_url):
    article_path = config.get_article_path(article_url)
    if not os.path.exists(article_path):
        return render_template(
            '404.html',
            title='Страница {} не найдена'.format(article_url),
            url=article_url
        )

    article_access_key = db.get_access_key(article_url)
    with open(article_path) as page:
        article_block = page.read()
    article = ArticleBlock(article_block)
    if request.cookies.get('access') == article_access_key:
        return render_template(
            'article-page.html',
            title=article.get_title(),
            content=article_block,
            is_author=True
        )
    else:
        return render_template(
            'article-page.html',
            title=article.get_title(),
            content=article_block
        )


@app.route('/<article_url>', methods=['POST'])
def content1(article_url):
    article_path = config.get_article_path(article_url)
    with open(article_path) as page:
        article_block = page.read()
    if request.form['state'] == 'edit article':
        article = ArticleBlock(article_block)
        return render_template(
            'form.html',
            title=article.get_title(),
            author=article.get_author(),
            article_text=article.get_markdown_content()
        )
    elif request.form['state'] == 'save article':
        form_data = dict(request.form)
        article = Article(
            form_data['title'][0],
            form_data['signature'][0],
            form_data['article'][0]
        )
        new_article_block = article.render_article_block()
        article.add_article_page(new_article_block, article_url)
        return render_template('article-page.html', title=article.title, content=new_article_block, is_author=True)
    else:
        return redirect(article_url)


if __name__ == "__main__":
    app.run()
