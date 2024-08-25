from store.utils import *
from store.extensions import db, Service, current_user

from ..models.OrdersModel import OrdersModel

class OrderService(Service):
    def __init__(self, store_id = None, order_id = None) -> None:
        self.orders = OrdersModel
        self.store_id = int(store_id) if store_id else None
        self.order_id = order_id or None

    def get_all(self):
        return db.session.query(OrdersModel).all()
    
    def delete():
        pass

    def get_by_store(self):
        return db.session.query(OrdersModel).where(OrdersModel.store_id == self.store_id).all()
    
    def get_by_id(self):
        return OrdersModel.query.where(OrdersModel.id == self.order_id).first()

    def save_db(self, store, file, data):
        Order = OrdersModel(
            store_id=store,
            file=file,
            order_content = f'{data}'
        )
        db.session.add(Order)
        db.session.commit()
        return Order
