from store.utils import *
from sqlalchemy import Column, Integer, LargeBinary,String


from store.extensions import db

from ...profile_image.view import LONGBLOB


class OrdersModel(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    store = relationship("Store", foreign_keys=[store_id])
    file = Column(LONGBLOB, nullable=False)
    create_at = Column(DateTime, default=func.now(),nullable=False)