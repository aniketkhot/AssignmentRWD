from flask import Blueprint, render_template, request, session, url_for

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

@bp.route('/basket/', methods= ['POST', 'GET'])
def basket():
    return render_template('basket.html')

# @bp.route('/deletebasket/')
# def deletebasket():
#     if 'basket_id' in session:
#         del session ['order_id']
#     return render_template('index.html')

# @bp.route('/deletebasketproduct/', methods = ['post'])
# def deletebasketproduct():
#     print ('user wants to delete tour with id={}'.format(request.form['id']))
#     return render_template('index.html')


@bp.route('/contactUs/', methods=['POST', 'GET'])
def contactUs():
    print('Email: {}\nName: {}\nPhoneNumber: {}\nShippingAdress: {}'\
          .format(request.values.get('email'), request.values.get('name'), request.values.get('phoneNumber'), request.values.get('shippingAdress')))
    return render_template('contactUs.html')

@bp.route('/aboutUs/')
def aboutUs():
    return render_template('aboutUs.html')


