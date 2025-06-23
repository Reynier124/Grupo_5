from typing import Type, List, Optional
from flask import Blueprint, jsonify, request, abort
from controllers.base_controller import BaseController
from schemas.base_schema import BaseSchema
from services.base_service import BaseService

class BaseControllerImpl(BaseController):
    """Base controller implementation."""

    def __init__(self, schema_in: Type[BaseSchema], schema_out: Optional[Type[BaseSchema]], service: BaseService):
        self.service = service
        self.schema_in = schema_in
        self.schema_out = schema_out
        self.blueprint = Blueprint('base', __name__)

        self.blueprint.add_url_rule("/", view_func=self.get_all, methods=["GET"])
        self.blueprint.add_url_rule("/<int:id_key>", view_func=self.get_one, methods=["GET"])
        self.blueprint.add_url_rule("/", view_func=self.save, methods=["POST"])
        self.blueprint.add_url_rule("/<int:id_key>", view_func=self.update, methods=["PUT"])
        self.blueprint.add_url_rule("/<int:id_key>", view_func=self.delete, methods=["DELETE"])

    @property
    def service(self) -> BaseService:
        """Service to access database."""
        return self._service

    @property
    def schema_in(self) -> Type[BaseSchema]:
        """Pydantic Schema to validate data."""
        return self._schema_in
    
    @property
    def schema_out(self) -> Type[BaseSchema]:
        """Pydantic Schema to validate data."""
        return self._schema_out


    def get_all(self):
        """Get all data."""
        items = self.service.get_all()
        return jsonify([self.schema_out.from_orm(item).dict() for item in items])

    def get_one(self, id_key: int):
        """Get one data."""
        item = self.service.get_one(id_key)
        if item is None:
            abort(404, description="Item not found")
        return self.schema_out.from_orm(item).dict()

    def save(self):
        """Save data."""
        schema_in = self.schema_in(**request.get_json())
        item = self.service.save(schema_in)
        return self.schema_out.from_orm(item).dict()

    def update(self, id_key: int):
        """Update data."""
        schema_in = self.schema_in(**request.get_json())
        item = self.service.update(id_key, schema_in)
        if item is None:
            abort(404, description="Item not found")
        return self.schema_out.from_orm(item).dict()

    def delete(self, id_key: int):
        """Delete data."""
        self.service.delete(id_key)
        return "", 204

    @schema_in.setter
    def schema_in(self, value):
        self._schema_in = value

    @schema_out.setter
    def schema_out(self, value):
        self._schema_out = value

    @service.setter
    def service(self, value):
        self._service = value