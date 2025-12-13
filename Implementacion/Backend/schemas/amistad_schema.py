from schemas.base_schema import BaseSchema
from typing import Optional
from datetime import datetime

class AmistadSchemaOut(BaseSchema):
    usuario_id: int
    amigo_id: int
    fecha_amistad: Optional[datetime] = None