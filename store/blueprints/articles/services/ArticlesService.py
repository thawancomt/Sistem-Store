from store.extensions import db
from ..models.ArticleModel import ArticleModel, TypeUnitModel

class ArticlesService:
    def __init__(self, name = None, description = None, type_unit= None, is_producible = None) -> None:
        self.name  = name
        self.description = description
        self.type_unit = type_unit
        self.is_producible = is_producible

    @staticmethod
    def get_all():
        return db.session.query(ArticleModel).all()
    
    @staticmethod
    def get_all_active():
        return db.session.query(ArticleModel).filter(ArticleModel.active == True).all()
    
    @staticmethod
    def get_all_producibles():
        return db.session.query(ArticleModel).filter(ArticleModel.is_producible == True).all()

    @staticmethod
    def get_all_stockable():
        return db.session.query(ArticleModel).filter(ArticleModel.stockable == True).all()
    
    # CRUD
    
    def create(self, data):
        new_article = ArticleModel()
        
        new_article.name = data.get('name')
        new_article.description = data.get('description')
        new_article.type_unit = data.get('type_unit')
        new_article.is_producible = bool(data.get('is_producible'))
        new_article.stockable = bool(data.get('is_stockable'))
        new_article.price = data.get('price')
        
        db.session.add(new_article)
        db.session.commit()
    


    def update(self, data):
        if article := self.get_by_id(data.get('article_id')):
            if article:
                article.name = data.get('name') or article.name
                article.description = data.get('description') or article.description
                article.type_unit = data.get('type_unit') or article.type_unit
                article.active = bool(data.get('active', 0))
                article.is_producible = bool(data.get('is_producible', 0))
                article.stockable = bool(data.get('is_stockable', 0))
                article.price = float(data.get('price')) or article.price
                
                db.session.commit()
                return True
        return False
    
    def delete(self, id):
        from store.blueprints.production.services.ProductionService import ProductionService
        from store.blueprints.stock.services.StockServices import StockServices
        
        if article := self.get_by_id(id):
            # Not recomende, may get server slow
            ProductionService().delete_all_production_by_article_id(id)
            StockServices().delete_all_stock_by_article_id(id)
            db.session.delete(article)
            db.session.commit()
            return True
        return False

    def get_by_id(self, id):
        return db.session.query(ArticleModel).filter(ArticleModel.id == id).first()


    
class TypeUnitsService:
    def __init__(self, name = None, alias = None, description = None) -> None:
        self.name = name, 
        self.alias = alias
        self.description = description 
        
    def create(self):
        new_type_unit = TypeUnitModel(name=self.name, alias=self.alias, description=self.description)
        db.session.add(new_type_unit)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return db.session.query(TypeUnitModel).all()
    
    
    # create a function that return fibonnaci sequence
    
    
    
