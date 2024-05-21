
from flaskr.blueprints import *
from flask import Blueprint, render_template, redirect, flash, url_for

from sqlalchemy.exc import IntegrityError

from ..services.ProductionService import ProductionService
from flaskr.extensions import db
from flask_login import login_required, current_user

from datetime import datetime


production = Blueprint('production', __name__, url_prefix='/production')


@production.route('/send', methods=['POST'])
@login_required
def send():
    item = request.form.get('item')
    amount = request.form.get('amount')

    production = ProductionService(item=item, amount=amount)
    
    if not production.get():
        production.send()
    
    else:
        flash('Item already exists', 'danger')
        production.update()
        
    return redirect(url_for('homepage.home'))


@production.route('/')
def view():
    return """
            <h1>Production</h1>
            """