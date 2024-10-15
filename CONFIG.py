from os import environ
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
HOST = '0.0.0.0'

USER, PWD, DB_HOST = environ.get('DB_USERNAME'), environ.get('DB_PWD'), environ.get('DB_HOST')


# Set the sqlachemy database URI
SQLALCHEMY_DATABASE_URI = f'sqlite:///teste.sqlite'


SQLALCHEMY_TRACK_MODIFICATIONS = False