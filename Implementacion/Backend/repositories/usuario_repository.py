from models.usuario import Usuario
from repositories.base_repository_impl import BaseRepositoryImpl, InstanceNotFoundError
from schemas.usuario_schema import UsuarioSchemaOut

class UsuarioRepository(BaseRepositoryImpl):
    def __init__(self):
        super().__init__(Usuario, UsuarioSchemaOut)
    
    def find_by_email(self, email: str):
        with self.session_scope() as session:
            model = session.query(self.model).get(email)
            if model is None:
                return None
            return self.schema.model_validate(model)