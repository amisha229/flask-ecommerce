# app/routes/main.py
from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.models import Product, Order

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@main_bp.route('/orders')
def orders():
    if 'user_id' not in session:
        flash('Please log in to view your orders.')
        return redirect(url_for('auth.login'))
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.order_date.desc()).all()
    return render_template('orders.html', orders=orders)

@main_bp.route('/health')
def health():
    return 'OK', 200