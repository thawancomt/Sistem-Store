from flaskr.blueprints import *
from flaskr.models.users import User, Session
from flaskr.models.production import Production
from datetime import datetime



bp_edit_user = Blueprint('edit_user', __name__, url_prefix='/edit')

def external_ip():
    return request.remote_addr

def is_user_logged_in(ip):
    # Check if user is logged in
    try:
        result = Session.connected_users[ip]['status']
        if result:
            return True
    except KeyError:
        return False
    
def user_data(date_for='', store_to_show=0):

    data = {}

    if not date_for:
        date_for = datetime.today()

    if store_to_show:
        data['total_of_the_day'] = Production(date_for).get_already_produced(store_to_show)
        data['store_name'] = Session(external_ip()).store_name()

    data['username'] = Session(external_ip()).name()
    data['level'] = Session(external_ip()).level()
    data['articles'] = Production.articles
    data['stores'] = Production.stores

    return data





@bp_edit_user.route('/<username>', methods=['GET', 'POST'])
def edit(username):
    

    # set old user
    old_user = User()
    old_user.username = username

    # after set old user, get their data
    old_data = User().get_user_data(old_user)

    # with his data define the old user email
    old_user.email = old_data['email']

    if request.method == 'POST':

        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        new_email = request.form.get('new_email')
        new_store = int(request.form.get('new_store'))

        new_data = {
            'username':  new_username,
            'password': new_password,
            'email': new_email,
            'store': new_store
        }

        User().edit_user(old_user, new_data)

        if username == user_data().get('username'):
            pass

        if new_username:
            return redirect(f'/{username}')
        else:
            return redirect(f'/{username}')

    context = {}
    context['data'] = user_data()
    context['old_data'] = old_data
    context['old_user'] = old_user
    context['username'] = username
    context['email'] = old_user.email

    return render_template("users/edit_user.html", context=context)