from store.blueprints import *
from ..services.StoreService import StoreService
from sqlalchemy.exc import IntegrityError

from flask_login import login_required

store = Blueprint('store', __name__, url_prefix='/store',
                  template_folder='../templates')

@store.route('/')
@login_required
def home():
    context = {
        'stores' : StoreService().get_all_stores()
    }
    return render_template('create_store.html', context=context)

@store.route('/create', methods=['POST'])
@login_required
def create():
    name = request.form['name']
    store_id = request.form['id']
    place = request.form['place']
    
    try:
        StoreService(store_id=store_id, store_name=name, store_place=place).create()

    except ValueError as e:
        flash(f'{e}')
    
    return redirect(url_for('store.home'))



