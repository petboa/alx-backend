#!/usr/bin/env python3
""" Flask barbel """
from flask import Flask, render_template
from flask_babel import Babel, request


class Config(object):
    """ Flask babel config """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Gets locale from query string"""
    req = request.query_string.decode("UTF-8").split("&")
    table = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        req,))
    if "locale" in table:
        if table["locale"] in Config.LANGUAGES:
            return table["locale"]
    return request.accept_languages.best_match(Config.LANGUAGES)


@app.route("/")
def Hello() -> str:
    """ Home page"""
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run()
