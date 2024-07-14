from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from ..Services.ShelLifeService import ShelLifeService

from flask_login import login_required, fresh_login_required


shelf_life = Blueprint('shelflife', __name__, template_folder='../templates',
                                                static_folder='../static',
                                                url_prefix='/shelf_life')


@shelf_life.route('/')
@login_required
def home():
    
    context = {
        'alerts' : ShelLifeService().get_by_date()
    }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    
    
    return render_template('shelf_life_home.html', context=context)
