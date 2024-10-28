from flask import Blueprint, render_template, request, session
from .model import Product, Basket, Category, ProductDetails, User


iphone18 = Product('1', 'Apple Iphone 18', 'wolrd class snapdragon 940 chipsent And adreno GPU. With all new apple 20 bionic chipset and 100MP camera', 2000 , 'apple bionic 20', 'Adreno', '100MP', '5000mah', '22 july 2018', 'iphone18.jpg')
iphone19 = Product('2', 'Apple Iphone 19', 'wolrd class snapdragon 940 chipsent And adreno GPU. With all new apple 20 bionic chipset and 100MP camera', 2000, 'apple bionic 20', 'Adreno', '100MP', '5000mah', '22 july 2018', 'iphone18.jpg')
iphone20 = Product('3', 'Apple Iphone 19', 'wolrd class snapdragon 940 chipsent And adreno GPU. With all new apple 20 bionic chipset and 100MP camera', 2000, 'apple bionic 20', 'Adreno', '100MP', '5000mah', '22 july 2018', 'iphone18.jpg')
iphone21 = Product('4', 'Apple Iphone 19', 'wolrd class snapdragon 940 chipsent And adreno GPU. With all new apple 20 bionic chipset and 100MP camera', 2000, 'apple bionic 20', 'Adreno', '100MP', '5000mah', '22 july 2018', 'iphone18.jpg')
iphone22 = Product('5', 'Apple Iphone 19', 'wolrd class snapdragon 940 chipsent And adreno GPU. With all new apple 20 bionic chipset and 100MP camera', 2000, 'apple bionic 20', 'Adreno', '100MP', '5000mah', '22 july 2018', 'iphone18.jpg')
iphone23 = Product('6', 'Apple Iphone 19', 'wolrd class snapdragon 940 chipsent And adreno GPU. With all new apple 20 bionic chipset and 100MP camera', 2000, 'apple bionic 20', 'Adreno', '100MP', '5000mah', '22 july 2018', 'iphone18.jpg')

products = [iphone18,iphone19,iphone20, iphone21, iphone22 ]

basket1 = Basket('1','10',[iphone18, iphone19,iphone20, iphone21],'scarletsBasket',0)
# basket2 = Basket('2','', '2', '', '')
# baskets = [basket1,basket2]




bp = Blueprint('main', __name__)



@bp.route('/')
def index():
    return render_template('index.html', products = products)


@bp.route('/details/<int:product_id>')
def details(product_id):
    print(product_id)
    for prod in products:
        if prod.id == product_id:
            return render_template('details.html', product = products)
        return "Product not found", 404


@bp.route('/basket/', methods= ['POST', 'GET'])
def basket():
    productId = request.args.get('productId')

    if 'basketId' not in session:
        session['basketId']=1

    # for i in baskets:
    #      if int(i.basketId) == int(session['basketId']):
    #          basket = i

    if productId:
        print(f'User requested to add tour id: {productId}')

    
    for d in basket1.products:
        print("dfdfdfdfdfdff")
        print(d.prize)
        basket1.totalCost += d.prize 

    

    return render_template('basket.html', somebasket = basket1)
    

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


