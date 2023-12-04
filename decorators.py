from System.managers.users import Session


def login_required():
    def verify_user_login():
        try:
            if Session.connected_users[ip]['status']:
                return True
        except KeyError:
            return False
