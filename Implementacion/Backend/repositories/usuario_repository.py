from models.usuario import Usuario, amistades
from repositories.base_repository_impl import BaseRepositoryImpl, InstanceNotFoundError
from schemas.usuario_schema import UsuarioSchemaOut
from schemas.amistad_schema import AmistadSchemaOut 
from datetime import datetime

class UsuarioRepository(BaseRepositoryImpl):
    def __init__(self, AmistadSchemaOut=AmistadSchemaOut):
        super().__init__(Usuario, UsuarioSchemaOut)
        self._schema_amistad = AmistadSchemaOut
        self._amistades_table = amistades
    
    def find_by_email(self, email: str):
        with self.session_scope() as session:
            model = session.query(self.model).get(email)
            if model is None:
                return None
            return self.schema.model_validate(model)
    
    def find_by_friendship(self, user_id: str, friend_id: str):
        with self.session_scope() as session:
            amistad = session.execute(
                self._amistades_table.select().where(
                    ((self._amistades_table.c.usuario_id == user_id) & (self._amistades_table.c.amigo_id == friend_id)) |
                    ((self._amistades_table.c.usuario_id == friend_id) & (self._amistades_table.c.amigo_id == user_id))
                )
            ).first()
            return self._schema_amistad.model_validate(amistad) if amistad else None
    
    def get_friends(self, user_id: int):
        with self.session_scope() as session:
            usuario = session.query(self.model).get(user_id)
            if not usuario:
                raise InstanceNotFoundError("Usuario no encontrado")
            # Convertir los amigos a schemas siguiendo el patrón de find_all
            schemas = []
            for amigo in usuario.amigos:
                schemas.append(self.schema.model_validate(amigo))
            return schemas
    
    def delete_friendship(self, user_id: str, friend_id: str):
        with self.session_scope() as session:
            amistad = session.execute(
                    self._amistades_table.delete().where(
                    ((self._amistades_table.c.usuario_id == user_id) & (self._amistades_table.c.amigo_id == friend_id)) |
                    ((self._amistades_table.c.usuario_id == friend_id) & (self._amistades_table.c.amigo_id == user_id))
                )
            )
            session.commit()
    
    def add_friendship(self, user_id: str, friend_id: str):
        with self.session_scope() as session:
            fecha = datetime.utcnow()
            nueva_amistad = self._amistades_table.insert().values(
                usuario_id=user_id,
                amigo_id=friend_id,
                fecha_amistad=fecha
            )
            session.execute(nueva_amistad)
            session.commit()
            amistad = AmistadSchemaOut(
                usuario_id=user_id,
                amigo_id=friend_id,
                fecha_amistad=fecha
            )
            return amistad