from flaskr.blueprints import *
from ..services.StoreService import StoreService
from sqlalchemy.exc import IntegrityError

store = Blueprint('store', __name__, url_prefix='/store',
                  template_folder='../templates')

@store.route('/')
def home():
    context = {
        'stores' : StoreService().get_all_stores()
    }
    return render_template('create_store.html', context=context)

@store.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    store_id = request.form['id']
    place = request.form['place']
    
    try:
        StoreService(store_id=store_id, store_name=name, store_place=place).create()

    except ValueError as e:
        flash(f'{e}')
    
    return redirect(url_for('store.home'))



