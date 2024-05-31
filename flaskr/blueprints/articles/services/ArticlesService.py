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