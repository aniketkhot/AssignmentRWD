from . import db
from datetime import date

# Many-to-Many Association Table for Orders and Products
order_products = db.Table(
    'order_products',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.order_id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.product_id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=1)
)



# Product Model
class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    price = db.Column(db.Float, nullable=False)
    cpu = db.Column(db.String(50), nullable=True)
    gpu = db.Column(db.String(50), nullable=True)
    camera = db.Column(db.String(50), nullable=True)
    battery = db.Column(db.String(50), nullable=True)
    release_date = db.Column(db.Date, default=date.today)
    image = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Product {self.product_id}: {self.name}, Price: {self.price}>"

# Order Model
class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    product_quantity_limit = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=True)
    products = db.relationship('Product', secondary=order_products, backref='orders')
    def __repr__(self):
        return f"<Order {self.order_id}, Total Cost: {self.total_cost}>"
