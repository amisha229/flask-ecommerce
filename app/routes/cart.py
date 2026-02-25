# app/routes/cart.py
from flask import Blueprint, session, redirect, url_for, flash, request, render_template
from app.models import Product
from app.models import Order, OrderItem, db
from flask import session

cart_bp = Blueprint('cart', __name__)

def get_cart():
    """Retrieve cart from session, initialise if not present."""
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def save_cart(cart):
    session['cart'] = cart
    session.modified = True

@cart_bp.route('/add/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = get_cart()
    # Check if product already in cart
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({'id': product_id, 'name': product.name, 'price': product.price, 'quantity': 1})
    save_cart(cart)
    flash(f'{product.name} added to cart.')
    return redirect(request.referrer or url_for('main.index'))

@cart_bp.route('/')
def view_cart():
    cart = get_cart()
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@cart_bp.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = get_cart()
    cart = [item for item in cart if item['id'] != product_id]
    save_cart(cart)
    flash('Item removed from cart.')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/update/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    quantity = int(request.form['quantity'])
    cart = get_cart()
    for item in cart:
        if item['id'] == product_id:
            if quantity <= 0:
                cart.remove(item)
            else:
                item['quantity'] = quantity
            break
    save_cart(cart)
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        flash('Please log in to checkout.')
        return redirect(url_for('auth.login'))
    
    cart = get_cart()
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('cart.view_cart'))
    
    # Calculate total once, used for both GET and POST
    total = sum(item['price'] * item['quantity'] for item in cart)

    if request.method == 'POST':
        # Create order
        order = Order(user_id=session['user_id'], total_amount=total)
        db.session.add(order)
        db.session.flush()  # to get order.id

        for item in cart:
            order_item = OrderItem(
                order_id=order.id,
                product_name=item['name'],
                product_price=item['price'],
                quantity=item['quantity']
            )
            db.session.add(order_item)

        db.session.commit()
        # Clear cart
        session.pop('cart', None)
        flash('Order placed successfully!')
        return redirect(url_for('main.orders'))

    # For GET request, just show the checkout page with cart and total
    return render_template('checkout.html', cart=cart, total=total)