from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Table
from datetime import datetime
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.ext.declarative import declared_attr

from models.base_model import BaseModel
from models.notificacion import Notificacion

amistades = Table('amistad', BaseModel.metadata,
    Column('usuario_id', String, ForeignKey('usuario.id'), primary_key=True),
    Column('amigo_id', String, ForeignKey('usuario.id'), primary_key=True),
    Column('fecha_amistad', DateTime, default=datetime.utcnow) 
)

class Usuario(BaseModel):
    __tablename__ = 'usuario'

    nombre = Column(String)
    email = Column(String)
    password = Column(String)
    rol = Column(String)
    
    amigos = relationship(
        "Usuario",
        secondary=amistades,
        primaryjoin=lambda: Usuario.id == foreign(amistades.c.usuario_id),
        secondaryjoin=lambda: Usuario.id == foreign(amistades.c.amigo_id),
        backref="amigos_de"
    )
    notificacion = relationship("Notificacion", back_populates="usuario")