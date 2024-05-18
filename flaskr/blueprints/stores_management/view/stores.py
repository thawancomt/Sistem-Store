from flaskr.blueprints import *
from flaskr.blueprints.stores_management.services.stores_service import StoresService
from sqlalchemy.exc import IntegrityError

store_bp = Blueprint('stores', __name__, url_prefix='/stores')

@store_bp.route('/')
def home():
    return render_template('store/create_store.html')

@store_bp.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    store_id = request.form['id']
    place = request.form['place']
    
    try:
        StoresService().create(name, store_id, place)
    
    except IntegrityError as e:
        flash(f'{e.orig}')
        return render_template('store/create_store.html', error=str(e))
    
    return render_template('store/create_store.html', name=name, id=id)


