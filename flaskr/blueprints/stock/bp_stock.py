from flaskr.blueprints import *


stock_bp = Blueprint('stock_bp', __name__, 
                    url_prefix='/stock')

@stock_bp.route('/')
def stock_page():
    return render_template('store/stock_page.html')