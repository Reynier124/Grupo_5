from controllers.base_controller_impl import BaseControllerImpl
from schemas.notificacion_schema import NotificacionSchemaIn, NotificacionSchemaOut
from services.notificacion_service import NotificacionService
from flask import Blueprint, jsonify, request, abort

class NotificacionController(BaseControllerImpl):
    def __init__(self):
        super().__init__(NotificacionSchemaIn, NotificacionSchemaOut, NotificacionService(), 'notificacion')
        self.blueprint.add_url_rule("/usuario/<int:id_key>", view_func=self.find_by_user, methods=["GET"])
        self.blueprint.add_url_rule("/enviar", view_func=self.enviar_notificacion, methods=["POST"])
        self.blueprint.add_url_rule("/marcar-leida/<int:id>", view_func=self.marcar_como_leida, methods=["PUT"]) 
 

    def find_by_user(self, id_key: int):
            items = self.service.get_by_user(str(id_key))
            if items is None:
                abort(404, description="Item not found")
            return jsonify([self.schema_out.from_orm(item).dict() for item in items])
    

    def enviar_notificacion(self):
        """
        Endpoint para enviar (crear) una notificación
        Body: {user_id, mensaje, tipo}
        """
        try:
            if not request.is_json:
                return jsonify({"error": "Content-Type debe ser application/json"}), 415
            data = self.schema_in(**request.get_json())
               
            # Enviar notificación a través del servicio
            notificacion = self.service.enviar_notificacion(data)
            
            return self.schema_out.from_orm(notificacion).dict(), 201
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": f"Error al enviar notificación: {str(e)}"}), 500
    
    def marcar_como_leida(self,id:int):
        """Marca una notificación como leída"""
        try:
            notificacion = self.service.marcar_como_leida(id)
            return self.schema_out.from_orm(notificacion).dict(), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": f"Error al marcar notificación: {str(e)}"}), 500

