from schemas.base_schema import BaseSchema

class UsuarioSchemaOut(BaseSchema):
    nombre : str
    email : str
    rol : str

class UsuarioSchemaIn(BaseSchema):
    nombre: str
    email: str
    password: str
    rol: str