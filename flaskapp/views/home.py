from flask import Blueprint, render_template


home = Blueprint('home', __name__)


@home.route('/')
def index():
    render_template("index.html")
