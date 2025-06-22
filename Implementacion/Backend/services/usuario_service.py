from services.base_service_impl import BaseServiceImpl
from repositories.usuario_repository import UsuarioRepository
from repositories.base_repository_impl import InstanceNotFoundError
from schemas.usuario_schema import UsuarioSchemaIn
from models.usuario import Usuario
from schemas.base_schema import BaseSchema
from werkzeug.security import generate_password_hash

class UsuarioService(BaseServiceImpl):
    def __init__(self):
        super().__init__(repository=UsuarioRepository(), model=Usuario, schema=UsuarioSchemaIn)
    
    def register_user(self, schema: BaseSchema):
        if self._repository.find_by_email(schema.email) is None:
            schema.password = generate_password_hash(schema.password)
            return self._repository.save(self.to_model(schema))
        else:
            raise ValueError("El email ya está registrado")

