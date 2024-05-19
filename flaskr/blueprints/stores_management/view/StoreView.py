from flaskr.blueprints import *
from ..services.StoreService import StoreService
from sqlalchemy.exc import IntegrityError

store = Blueprint('store', __name__, url_prefix='/store')

@store.route('/')
def home():
    return render_template('store/create_store.html')

@store.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    store_id = request.form['id']
    place = request.form['place']
    
    try:
        StoreService(name, store_id, place).create()
    except IntegrityError as e:
        flash(f'{e.orig}')
        return render_template('store/create_store.html', error=str(e))
    
    return render_template('store/create_store.html', name=name, id=id)


