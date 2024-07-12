from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from ..Services.ShelLifeService import ShelLifeService



shelf_life = Blueprint('shelflife', __name__, template_folder='../templates',
                                                static_folder='../static',
                                                url_prefix='/shelf_life')


@shelf_life.route('/')
def home():
    
    context = {
        'alerts' : ShelLifeService().get_by_date()
    }
    
    
    return render_template('home.html', context=context)
