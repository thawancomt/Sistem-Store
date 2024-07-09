from flask import Blueprint, render_template, url_for, g, request, send_file

from pathlib import Path

from io import BytesIO

from store.extensions import db
from sqlalchemy import Column, Integer, LargeBinary,String
from sqlalchemy.dialects.mysql import LONGBLOB

profile_image = Blueprint('profile_image', __name__,
                          url_prefix='/profile_image',
                          template_folder='./')


class File(db.Model):
    id = Column(Integer, primary_key=True)
    filename = Column(String(100), nullable=False)
    data = Column(LONGBLOB, nullable=False)


@profile_image.route('/')
def home():
    return render_template('index.html')

@profile_image.route('/', methods=['POST'])
def save():
    file = request.files.get('file')
    filename = file.filename

    path = Path(__file__).parent.resolve() / filename


    new_file = File()
    new_file.filename = filename
    new_file.data = file.read()

    db.session.add(new_file)
    db.session.commit()


    return render_template('index.html', id=new_file.id)

@profile_image.route('/get/<id>')
def view(id):
    file = db.session.query(File).where(File.id == id).first()
    return send_file(BytesIO(file.data), download_name=file.filename)