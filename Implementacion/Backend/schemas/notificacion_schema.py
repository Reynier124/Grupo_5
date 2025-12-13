from datetime import datetime
from schemas.base_schema import BaseSchema

class NotificacionSchemaOut(BaseSchema):
    tipo : str
    mensaje : str
    fecha_hora : datetime
    leida : bool
    usuario_id : int

class NotificacionSchemaIn(BaseSchema):
    tipo : str
    mensaje : str
    destinatario : int