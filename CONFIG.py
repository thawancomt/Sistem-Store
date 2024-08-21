from os import environ

DEBUG = True
HOST = '0.0.0.0'

USER, PWD, DB_HOST = environ.get('DB_USERNAME'), environ.get('DB_PWD'), environ.get('DB_HOST')


# Set the sqlachemy database URI
SQLALCHEMY_DATABASE_URI = f'mysql://{USER}:{PWD}@{DB_HOST}/storedb'


SQLALCHEMY_TRACK_MODIFICATIONS = False