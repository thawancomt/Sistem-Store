from flaskr.extensions import db
from ..models.ArticleModel import ArticleModel, TypeUnitModel

class ArticlesService:
    def __init__(self, name = None, description = None, type_unit= None, is_producible = None) -> None:
        self.name  = name
        self.description = description
        self.type_unit = type_unit
        self.is_producible = is_producible

    def create(self):
        new_article = ArticleModel(name=self.name,
                                   description=self.description,
                                   type_unit=self.type_unit,
                                   is_producible = self.is_producible
                                )
        db.session.add(new_article)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return db.session.query(ArticleModel).all()
    
    @staticmethod
    def get_all_producibles():
        return db.session.query(ArticleModel).filter(ArticleModel.is_producible == True).all()

    @staticmethod
    def get_all_stockable():
        return db.session.query(ArticleModel).filter(ArticleModel.stockable == True).all()


    def edit_article(self, data):
        if article := db.session.query(ArticleModel).filter(ArticleModel.id == data['article_id']).first():
            article.name = data['name']
            article.description = data['description']
            article.type_unit = data['type_unit']
            article.is_producible = bool(data.get('is_producible', 0))
            article.stockable = bool(data.get('stockable', 0))
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
    
    