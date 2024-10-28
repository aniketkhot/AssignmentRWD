from flask import Blueprint, render_template, request, session, flash, redirect, url_for, abort
from .model import Product, Order, order_products
from . import db

bp = Blueprint('main', __name__)

# Index page displaying all products with search and filter functionality
@bp.route('/')
def index():
    search_query = request.args.get('search')
    sort_option = request.args.get('sort')
    brand = request.args.get('brand')

    # Start with base query for all products
    query = db.select(Product)

    # Apply search filter if a search term is entered
    if search_query:
        query = query.where(Product.name.ilike(f"%{search_query}%"))

    # Apply brand filter if a brand is specified
    if brand:
        query = query.where(Product.brand.ilike(f"%{brand}%"))

    # Apply sorting based on user selection
    if sort_option == 'high_to_low':
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
    try:
        basket_order = db.session.get(Order, session.get('order_id'))
        
        if not basket_order:
            basket_order = Order(product_quantity_limit=10, total_cost=0)
            db.session.add(basket_order)
            db.session.commit()
            session['order_id'] = basket_order.order_id

        existing_product = db.session.execute(
            db.select(order_products).filter_by(order_id=basket_order.order_id, product_id=product_id)
        ).fetchone()

        if existing_product:
            db.session.execute(
                db.update(order_products)
                .where(order_products.c.order_id == basket_order.order_id, order_products.c.product_id == product_id)
                .values(quantity=existing_product.quantity + 1)
            )
        else:
            db.session.execute(
                order_products.insert().values(order_id=basket_order.order_id, product_id=product_id, quantity=1)
            )
        
        db.session.commit()
        flash("Product added to basket successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")
    finally:
        db.session.close()
    
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

    total_cost = sum(product.price * quantity for product, quantity in products)
    order.total_cost = total_cost
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
    elif action == "decrement" and current_quantity > 1:
        new_quantity = current_quantity - 1
    else:
        new_quantity = current_quantity

    db.session.execute(
        db.update(order_products)
        .where(order_products.c.order_id == order_id, order_products.c.product_id == product_id)
        .values(quantity=new_quantity)
    )

    order = db.session.get(Order, order_id)
    order.total_cost += (new_quantity - current_quantity) * product.price
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

    order.total_cost -= product.price * quantity
    db.session.commit()

    flash(f'Removed {product.name} from basket.')
    return redirect(url_for('main.basket'))
