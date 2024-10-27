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

@bp.route('/basket/')
def basket():
    return render_template('basket.html')

@bp.route('/contactUs/')
def contactUs():
    return render_template('contactUs.html')

@bp.route('/aboutUs/')
def aboutUs():
    return render_template('aboutUs.html')


