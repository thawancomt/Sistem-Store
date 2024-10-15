from store.utils import *
from sqlalchemy import Column, Integer, LargeBinary, String, BLOB, Text, DateTime, ForeignKey, BOOLEAN
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from store.extensions import db

class OrdersModel(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    store = relationship("Store", foreign_keys=[store_id])
    order_content = Column(Text, nullable=False)
    file = Column(BLOB, nullable=False)
    accepted = Column(BOOLEAN, server_default="0", nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)