# Store
from store.blueprints.stores_management.models.StoreModel import Store

# User
from store.blueprints.users.models.UserModel import User
from store.blueprints.users.services.UserService import generate_password_hash, check_password_hash



from store.extensions import db

def check_store():
    if not Store.query.all():
        create_example_store()

def create_example_store():
        example_store = Store(
            id = 49,
            name = 'Pink New york pizza',
            place = 'street'

        )
        db.session().add(example_store)
        db.session.commit()

def check_user():
    if not User.query.first():
        create_example_user()
    
def create_example_user():
    example_user_admin = User(
                username = 'admin',
                email = 'admin@gmail.com',
                level = 0,
                password = generate_password_hash('admin'),
                store_id = 49,
                last_login = '2003-12-12',
                created_at = '2003-12-12',
                active = 1
            )
    db.session.add(example_user_admin)
    db.session.commit()


