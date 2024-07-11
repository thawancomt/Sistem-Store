from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from store.blueprints.users.services.UserService import UserService, generate_password_hash, check_password_hash
from store.extensions import db

from random import randint


class CodeModel(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(256), nullable=False)
    date = Column(DateTime, server_default=func.now())
    
    user_id = Column(ForeignKey('users.id'), nullable=False)
    
    user = relationship('User', foreign_keys=[user_id])
    

class CodeService:
    def __init__(self, id = None) -> None:
        
        self.user = UserService.get(id)
        self.code = randint(100000, 999999)
        self._no_hashed_code = self.code
        self.insert_new_code()
        
        # 1 step - Take the user
        # 2 step - Generate a code
        # 3 step - Load the code to a variable no hashed
        # 4 step - Insert the new code into the table
    
    def insert_new_code(self):
        if not (code := db.session.query(CodeModel).where(CodeModel.user_id == self.user.id).first()):
            code = CodeModel()
            code.user_id = self.user.id

        code.code = generate_password_hash(str(self.code))
        code.date = func.now()
        db.session.add(code)
        db.session.commit()
        return code
    @staticmethod
    def check_code(id, code) -> bool:
        if usercode := db.session.query(CodeModel).where(CodeModel.user_id == id).first():
            if check_password_hash(usercode.code, str(code)):
                return True
        return False