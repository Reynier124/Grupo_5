from services.base_service_impl import BaseServiceImpl
from repositories.usuario_repository import UsuarioRepository
from repositories.base_repository_impl import InstanceNotFoundError
from schemas.usuario_schema import UsuarioSchemaIn
from models.usuario import Usuario, amistades
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

    def get_amigos(self, user_id):
        """Obtiene los amigos de un usuario"""
        usuario = self.repository.get_friends(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        friends = self.repository.get_friends(user_id)
        return friends
    
    def eliminar_amigo(self, user_id:int, friend_id:int):
        """Elimina un amigo"""
        # Verificar que ambos usuarios existen
        usuario = self.repository.find(user_id)
        amigo = self.repository.find(friend_id)
        
        if not usuario or not amigo:
            raise ValueError("Usuario no encontrado")
        
        amistad_existente = self.repository.find_by_friendship(user_id, friend_id)
        
        if not amistad_existente:
            raise ValueError("Amistad no encontrada")
        
        self.repository.delete_friendship(user_id, friend_id)
        
        # Retornar info del amigo eliminado (para crear la notificación en el frontend)
        return {'message': 'Amigo eliminado correctamente'}
    
    def agregar_amigo(self, user_id, friend_id):
        """Agrega un amigo"""
        # Verificar que ambos usuarios existen
        usuario = self.repository.find(user_id)
        amigo = self.repository.find(friend_id)
        
        if not usuario or not amigo:
            raise ValueError("Usuario no encontrado")
        
        amistad_existente = self.repository.find_by_friendship(user_id, friend_id)
        if amistad_existente:
            raise ValueError("La amistad ya existe")
        
        # Agregar la amistad
        amistad = self.repository.add_friendship(user_id, friend_id)
        return {
            'message': 'Amigo agregado correctamente',
            'results': amistad
        }