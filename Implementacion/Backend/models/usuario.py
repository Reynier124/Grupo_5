from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declared_attr

from models.base_model import BaseModel

class Usuario(BaseModel):
    __tablename__ = 'usuario'

    nombre = Column(String)
    email = Column(String)
    password = Column(String)
    rol = Column(String)