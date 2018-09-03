# browser-sync start --proxy "127.0.0.1:5000" --files "static/**/*, templates/*.html, *.py"
import os
from flask import Flask, render_template, request, redirect, make_response
from flask_simplemde import SimpleMDE
from flask_wtf import CSRFProtect
from flask_sslify import SSLify


import config
import db
from models import Article
app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(config.DevelopmentConfig)
SimpleMDE(app)
sslify = SSLify(app)

try:
    os.mkdir(os.path.join(config.basedir, 'articles'))
except OSError:
    pass


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        article = Article(
            request.form['title'],
            request.form['plan'].replace('\r\n', '\n'),
            request.form['plan_html'].replace('\r\n', '\n'),
            request.form['article'].replace('\r\n', '\n'),
            request.form['article_html'].replace('\r\n', '\n')
        )

        article_block = article.render_article_block()
        article.add_article_page(article_block, article.url)
        response = make_response(redirect(article.url))
        article.add_article_to_db()
        return response

    return render_template('form.html')


@app.route('/<article_url>', methods=['GET'])
def content(article_url):
    if not config.has_file(article_url):
        return render_template(
            '404.html',
            title='Страница {} не найдена'.format(article_url),
            url=article_url
        )
    article_path = config.get_article_path(article_url)
    with open(article_path) as page:
        article_block = page.read()
    return render_template(
        'article-page.html',
        title=db.get_article(article_url).title,
        content=article_block
    )


@app.route('/<article_url>', methods=['POST'])
def content1(article_url):
    article = db.get_article(article_url)
    if request.form['state'] == 'edit article':
        return render_template(
            'form.html',
            title=article.title,
            plan=article.plan,
            article_text=article.text
        )
    elif request.form['state'] == 'save article':
        article = Article(
            request.form['title'],
            request.form['plan'].replace('\r\n', '\n'),
            request.form['plan_html'].replace('\r\n', '\n'),
            request.form['article'].replace('\r\n', '\n'),
            request.form['article_html'].replace('\r\n', '\n')
        )
        article.url = article_url
        new_article_block = article.render_article_block()
        article.add_article_page(new_article_block, article_url)
        article.add_article_to_db()
        return render_template('article-page.html', title=article.title, content=new_article_block)
    else:
        return redirect(article_url)


if __name__ == "__main__":
    app.run(debug=True)
