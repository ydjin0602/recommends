from flask import Flask

from recommends.view import RecommendsView

app = Flask(__name__)
app.add_url_rule('/', view_func=RecommendsView.as_view(''))


if __name__ == '__main__':
    app.run()
