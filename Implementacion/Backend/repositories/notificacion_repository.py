from models.notificacion import Notificacion
from repositories.base_repository_impl import BaseRepositoryImpl, InstanceNotFoundError
from schemas.notificacion_schema import NotificacionSchemaOut, NotificacionSchemaIn

class NotificacionRepository(BaseRepositoryImpl):
    def __init__(self):
        super().__init__(Notificacion, NotificacionSchemaOut)

    def find_by_user(self, destinatario: str):
        with self.session_scope() as session:
            modelos = (
                session.query(self.model)
                .filter(self.model.usuario_id == destinatario)
                .all()
            )
            if not modelos:
                return []
            return [self.schema.model_validate(m) for m in modelos]