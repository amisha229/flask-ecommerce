# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app import db
from app.models import Product
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('You need admin privileges to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/add_product', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        image_url = request.form['image_url']
        product = Product(name=name, price=price, description=description, image_url=image_url)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.')
        return redirect(url_for('admin.add_product'))
    return render_template('admin/add_product.html')