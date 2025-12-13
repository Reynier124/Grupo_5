from controllers.base_controller_impl import BaseControllerImpl
from schemas.usuario_schema import UsuarioSchemaIn, UsuarioSchemaOut
from schemas.amistad_schema import AmistadSchemaOut
from services.usuario_service import UsuarioService
from flask import Blueprint, jsonify, request, abort

class UsuarioController(BaseControllerImpl):
    def __init__(self):
        super().__init__(UsuarioSchemaIn, UsuarioSchemaOut, UsuarioService(), 'usuario')
        self._amistad_schema = AmistadSchemaOut
        self.blueprint.add_url_rule("/register", view_func=self.register, methods=["POST"])
        self.blueprint.add_url_rule("/amigos", view_func=self.agregar_amigo, methods=["POST"])
        self.blueprint.add_url_rule("/amigos/<int:id>", view_func=self.get_amigos, methods=["GET"])
        self.blueprint.add_url_rule("<int:user_id>/amigos/<int:friend_id>", view_func=self.eliminar_amigo, methods=["DELETE"])
    
    def register(self):
        schema = self.schema_in(**request.get_json())
        item = self.service.register_user(schema)
        return self.schema_out.from_orm(item).dict(), 409
    
    def get_amigos(self, id):
        try:
            amigos = self.service.get_amigos(id)
            return jsonify([self.schema_out.from_orm(amigo).dict() for amigo in amigos]), 200
        except ValueError as e:
            abort(404, description=str(e))

    def eliminar_amigo(self, user_id, friend_id):
        try:
            result = self.service.eliminar_amigo(user_id, friend_id)
            return result, 200
        except ValueError as e:
            abort(404, description=str(e))
    
    def agregar_amigo(self):
        data = request.get_json()
        try:
            result = self.service.agregar_amigo(data['user_id'], data['friend_id'])
            return {
            "message": result["message"],
            "results": self._amistad_schema.model_validate(result["results"]).dict()
            }, 201
        except ValueError as e:
            abort(404, description=str(e))