from services.base_service_impl import BaseServiceImpl
from repositories.notificacion_repository import NotificacionRepository
from repositories.usuario_repository import UsuarioRepository
from datetime import datetime
from repositories.base_repository_impl import InstanceNotFoundError
from schemas.notificacion_schema import NotificacionSchemaIn, NotificacionSchemaOut
from models.notificacion import Notificacion
from schemas.base_schema import BaseSchema

class NotificacionService(BaseServiceImpl):
    def __init__(self):
        super().__init__(repository=NotificacionRepository(), model=Notificacion, schema=NotificacionSchemaIn)
        self.usuario_repository = UsuarioRepository()

    def get_by_user(self, destinatario: str):
        """Return all notifications for a specific user."""
        return self.repository.find_by_user(destinatario)

    def enviar_notificacion(self, notificacion_data):
        user_id = notificacion_data.destinatario
        print(user_id)
        # [OBSERVER - Paso 5] NotificacionService valida usuario: get() → UsuarioRepository → retorna user (Paso 6)
        usuario = self.usuario_repository.find(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # [OBSERVER - Paso 7] Creando notificacion (self-call en el diagrama: NotificacionRepository instancia el objeto)
        notificacion = Notificacion(
            usuario_id=user_id,
            mensaje=notificacion_data.mensaje,
            tipo=notificacion_data.tipo,
            leida=False,
            fecha_hora=datetime.utcnow()
        )

        # [OBSERVER - Paso 7] NotificacionService → NotificacionRepository: save notification()
        notificacion_guardada = self.repository.save(notificacion)

        # [OBSERVER - Paso 8] Retorna schema al NotificacionController
        return notificacion_guardada
      
    def marcar_como_leida(self, id: int):
        """Marca una notificación como leída"""
        notificacion = self.repository.find(id)
        if not notificacion:
            raise ValueError("Notificación no encontrada")
        
        notificacion.leida = True
        notificacion_actualizada = self.repository.update(id, notificacion.model_dump())
        return notificacion_actualizada
