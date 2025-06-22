from controllers.base_controller_impl import BaseControllerImpl
from schemas.usuario_schema import UsuarioSchemaIn, UsuarioSchemaOut
from services.usuario_service import UsuarioService
from flask import Blueprint, jsonify, request, abort

class UsuarioController(BaseControllerImpl):
    def __init__(self):
        super().__init__(UsuarioSchemaIn, UsuarioSchemaOut, UsuarioService())
        self.blueprint.add_url_rule("/register", view_func=self.register, methods=["POST"])
    
    def register(self):
        schema = self.schema_in(**request.get_json())
        item = self.service.register_user(schema)
        return self.schema_out.from_orm(item).dict(), 409