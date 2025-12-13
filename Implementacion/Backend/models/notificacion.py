from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from models.base_model import BaseModel

class Notificacion(BaseModel):
    __tablename__ = 'notificacion'

    tipo = Column(String)
    mensaje = Column(String)
    fecha_hora = Column(DateTime)
    leida = Column(Boolean, default=False)
    usuario_id = Column(String, ForeignKey('usuario.id'))
    usuario = relationship("Usuario", back_populates="notificacion")