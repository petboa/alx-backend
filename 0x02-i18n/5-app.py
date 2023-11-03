#!/usr/bin/env python3
""" Flask barbel """
from flask import Flask, render_template, g
from flask_babel import Babel, request
from typing import Dict, Union


class Config(object):
    """ Flask babel config """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(login_as: str) -> Union[Dict, None]:
    """Gets the user based on id """
    try:
        return users.get(int(login_as))
    except Exception:
        return


@app.before_request
def before_request() -> None:
    """ Sets up routes """
    g.user = get_user(request.args.get("login_as"))


@babel.localeselector
def get_locale() -> str:
    """Gets locale from query string"""
    locale = request.args.get("locale")
    if locale:
        return locale
    user = request.args.get("login_as")
    if user:
        lang = users.get(int(user)).get('locale')
        if lang in Config.LANGUAGES:
            return lang
    headers = request.headers.get("locale")
    if headers:
        return headers
    return request.accept_languages.best_match(Config.LANGUAGES)


@app.route("/")
def Hello() -> str:
    """ Home page"""
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run()
