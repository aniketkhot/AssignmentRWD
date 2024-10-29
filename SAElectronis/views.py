from flask import Blueprint, render_template, request, session, flash, redirect, url_for, abort, g
from .model import Product, Order, order_products
from . import db
from datetime import datetime, timedelta


bp = Blueprint('main', __name__)


@bp.before_app_request
def load_basket_quantity():
    order_id = session.get('order_id')
    if order_id:
        order = db.session.get(Order, order_id)
        g.basket_quantity = order.product_quantity if order else 0
    else:
        g.basket_quantity = 0

# Index page
@bp.route('/')
def index():
    search_query = request.args.get('search')
    sort_option = request.args.get('sort')
    brand = request.args.get('brand')  # Get brand parameter from URL
    recent_launches = request.args.get('recent_launches')  # Get recent_launches parameter

    # Start with base query for all products
    query = db.select(Product)

    # Apply search filter if a search term is entered
    if search_query:
        query = query.where(Product.name.ilike(f"%{search_query}%"))

    # Apply brand filter if a brand is specified
    if brand:
        query = query.where(Product.name.ilike(f"%{brand}%"))

    # Apply recent launches filter with specified time frame
    if recent_launches:
        # Define the time frame based on the recent_launches parameter
        if recent_launches == '3_months':
            time_threshold = datetime.now() - timedelta(days=90)
        elif recent_launches == '6_months':
            time_threshold = datetime.now() - timedelta(days=180)
        elif recent_launches == '1_year':
            time_threshold = datetime.now() - timedelta(days=365)
        elif recent_launches == '3_years':
            time_threshold = datetime.now() - timedelta(days=365 * 3)
        elif recent_launches == '5_years':
            time_threshold = datetime.now() - timedelta(days=365 * 5)
        elif recent_launches == 'all_time':
            time_threshold = None  # No date filter for all time
        else:
            time_threshold = None
        # Filter products by release date if a valid time frame is set
        if time_threshold:
            query = query.where(Product.release_date >= time_threshold)
            query = query.order_by(Product.release_date.desc())  # Order by release date, newest first

    # Apply sorting based on user selection if recent_launches is not set
    elif sort_option == 'high_to_low':
        query = query.order_by(Product.price.desc())
    elif sort_option == 'low_to_high':
        query = query.order_by(Product.price.asc())

    products = db.session.scalars(query).all()
    return render_template('index.html', products=products)

# Product details page
@bp.route('/details/<int:product_id>')
def details(product_id):
    product = db.session.scalars(db.select(Product).where(Product.product_id == product_id)).first()
    if product is None:
        return "Product not found", 404
    return render_template('details.html', product=product)

# Add product to basket
@bp.route('/add_to_basket/<int:product_id>', methods=['POST'])
def add_to_basket(product_id):
    
    basket_order = db.session.get(Order, session.get('order_id'))
    
    if not basket_order:
        basket_order = Order(product_quantity=0, total_cost=0)  
        db.session.add(basket_order)
        db.session.commit()
        session['order_id'] = basket_order.order_id

    # Check if the product is already in the order
    existing_product = db.session.execute(
        db.select(order_products).filter_by(order_id=basket_order.order_id, product_id=product_id)
    ).fetchone()

    if existing_product:            
        new_quantity = existing_product.quantity + 1
        db.session.execute(
            db.update(order_products)
            .where(order_products.c.order_id == basket_order.order_id, order_products.c.product_id == product_id)
            .values(quantity=new_quantity)
        )
    else:
        db.session.execute(
            order_products.insert().values(order_id=basket_order.order_id, product_id=product_id, quantity=1)
        )
    basket_order.product_quantity += 1
    basket_order.total_cost += db.session.get(Product, product_id).price
    db.session.commit()

    flash("Product added to basket successfully", "success")
    return redirect(url_for('main.index'))


# View basket
@bp.route('/basket')
def basket():
    order_id = session.get('order_id')
    if order_id is None:
        return render_template('basket.html', products=[], total_cost=0)

    order = db.session.get(Order, order_id)
    if not order:
        return render_template('basket.html', products=[], total_cost=0)

    products = db.session.execute(
        db.select(Product, order_products.c.quantity)
        .join(order_products, Product.product_id == order_products.c.product_id)
        .where(order_products.c.order_id == order_id)
    ).all()

    # Calculate the total cost and total quantity
    total_cost = sum(product.price * quantity for product, quantity in products)
    total_quantity = sum(quantity for _, quantity in products)

    # Update the order with the calculated total cost and total quantity
    order.total_cost = total_cost
    order.product_quantity = total_quantity
    db.session.commit()

    return render_template('basket.html', products=products, total_cost=total_cost)

# Update quantity of a product in the basket
@bp.route('/update_quantity/<int:product_id>/<string:action>', methods=['POST'])
def update_quantity(product_id, action):
    order_id = session.get('order_id')
    if not order_id:
        abort(404)

    product = db.session.get(Product, product_id)
    if not product:
        abort(404)

    current_quantity = db.session.execute(
        db.select(order_products.c.quantity)
        .where(order_products.c.order_id == order_id, order_products.c.product_id == product_id)
    ).scalar()

    if action == "increment":
        new_quantity = current_quantity + 1
        quantity_change = 1
    elif action == "decrement" and current_quantity > 1:
        new_quantity = current_quantity - 1
        quantity_change = -1
    else:
        new_quantity = current_quantity
        quantity_change = 0

    db.session.execute(
        db.update(order_products)
        .where(order_products.c.order_id == order_id, order_products.c.product_id == product_id)
        .values(quantity=new_quantity)
    )

    # Update order total cost and quantity
    order = db.session.get(Order, order_id)
    order.total_cost += quantity_change * product.price
    order.product_quantity += quantity_change
    db.session.commit()

    return redirect(url_for('main.basket'))


# Remove product from basket
@bp.route('/remove_from_basket/<int:product_id>', methods=['POST'])
def remove_from_basket(product_id):
    order_id = session.get('order_id')
    if not order_id:
        abort(404)

    order = db.session.get(Order, order_id)
    if not order:
        abort(404)

    product = db.session.get(Product, product_id)
    if not product:
        abort(404)

    quantity = db.session.execute(
        db.select(order_products.c.quantity)
        .where(order_products.c.order_id == order_id, order_products.c.product_id == product_id)
    ).scalar()

    db.session.execute(
        order_products.delete().where(
            order_products.c.order_id == order_id,
            order_products.c.product_id == product_id
        )
    )

    # Update order's total cost and total quantity
    order.total_cost -= product.price * quantity
    order.product_quantity -= quantity
    db.session.commit()

    flash(f'Removed {product.name} from basket.')
    return redirect(url_for('main.basket'))


# Contact Us route
@bp.route('/contact')
def contact():
    return render_template('contactUs.html')

# Checkout route
@bp.route('/checkout')
def checkout():
    # Retrieve total cost from the GET request or set default if not present
    total_cost = request.args.get('total_cost', type=float, default=0)
    return render_template('checkout.html', total_cost=total_cost)

# About Us route
@bp.route('/about')
def about():
    return render_template('aboutUs.html')