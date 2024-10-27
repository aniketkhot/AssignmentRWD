from flask import Blueprint, render_template, request, session
from .model import Product


iphone18 = Product('1', 'Apple Iphone 18', 'wolrd class snapdragon 940 chipsent And adreno GPU. With all new apple 20 bionic chipset and 100MP camera', '2000 AUD', 'apple bionic 20', 'Adreno', '100MP', '5000mah', '22 july 2018', 'iphone18.jpg')
iphone19 = Product('2', 'Apple Iphone 19', 'wolrd class snapdragon 940 chipsent And adreno GPU. With all new apple 20 bionic chipset and 100MP camera', '2000 AUD', 'apple bionic 20', 'Adreno', '100MP', '5000mah', '22 july 2018', 'iphone18.jpg')

products = [iphone18,iphone19,iphone18,iphone18,iphone18,iphone19,iphone18,iphone18  ]


bp = Blueprint('main', __name__)



@bp.route('/')
def index():
    return render_template('index.html', products = products)


@bp.route('/item/<int:product_id>')
def item(product_id):
    return render_template('item.html', product_id = product_id)

@bp.route('/details/')
def details():
    return render_template('details.html')

@bp.route('/basket/', methods= ['POST', 'GET'])
def basket():
    return render_template('basket.html')

@bp.route('/deletebasket/')
def deletebasket():
     if 'basket_id' in session:
         del session ['order_id']
     return render_template('index.html')

@bp.route('/deletebasketproduct/', methods = ['post'])
def deletebasketproduct():
     print (f'user wants to delete product with id={request.form['id']}')
     return render_template('index.html')


@bp.route('/contactUs/', methods=['POST', 'GET'])
def contactUs():
    print('Email: {}\nName: {}\nPhoneNumber: {}\nShippingAdress: {}'\
          .format(request.values.get('email'), request.values.get('name'), request.values.get('phoneNumber'), request.values.get('shippingAdress')))
    return render_template('contactUs.html')

@bp.route('/aboutUs/')
def aboutUs():
    return render_template('aboutUs.html')


