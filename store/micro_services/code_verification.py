from store.extensions import db

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship


from store.blueprints.users.services.UserService import UserService, generate_password_hash, check_password_hash


from random import randint


class CodeModel(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(256), nullable=False)
    date = Column(DateTime, server_default=func.now())
    
    user_id = Column(ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', foreign_keys=[user_id])
    

class CodeService:
    def __init__(self, id = None) -> None:
        if not id:
            return False
        
        self.user = UserService.get(id)
        self.code = randint(100000, 999999)
        self._code = self.code
    
    def insert_new_code(self):
        
        if not (
            code := db.session.query(CodeModel)
            .where(CodeModel.user_id == self.user.id)
            .first()
        ):
            code = CodeModel()
            code.user_id = self.user.id

        code.code = generate_password_hash(str(self.code))
        code.date = func.now()
        db.session.add(code)
        db.session.commit()
        return code
    
    def check_code(self, code):
        if usercode := db.session.query(CodeModel).where(CodeModel.user_id == self.user.id).first():
            if check_password_hash(usercode.code, str(code)):
                return True
        return False