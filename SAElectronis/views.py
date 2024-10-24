from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/item/')
def item():
    return render_template('item.html')

@bp.route('/details/')
def details():
    return render_template('details.html')