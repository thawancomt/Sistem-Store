from store.utils import *


from store.extensions import db


class OrdersModel(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    store = relationship("Store", foreign_keys=[store_id])
    file = Column(BLOB, nullable=False)
    create_at = Column(DateTime, nullable=False)