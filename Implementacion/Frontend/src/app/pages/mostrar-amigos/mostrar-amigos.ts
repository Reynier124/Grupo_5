import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { ServicioUsuario } from '../../services/servicio-usuario';
import { ServicioNotificacion } from '../../services/servicio-notificacion';

@Component({
  selector: 'app-mostrar-amigos',
  standalone: false,
  templateUrl: './mostrar-amigos.html',
  styleUrl: './mostrar-amigos.css'
})
export class MostrarAmigos {
  friends: any[] = [];
  notifications: any[] = [];
  userId: number = 0; // ID del usuario actual
  private notificationSubscription!: Subscription;

  constructor(
    private usuarioService: ServicioUsuario,
    private notificationService: ServicioNotificacion,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
    this.userId = Number(params.get('id'));
    this.loadFriends();
    this.loadNotifications();
    });

    // PATRÓN OBSERVER: Suscribirse a nuevas notificaciones
    this.notificationSubscription = this.notificationService
      .getNotificationObservable()
      .subscribe(notification => {
        this.notifications.unshift(notification);
      });
  }

  ngOnDestroy(): void {
    if (this.notificationSubscription) {
      this.notificationSubscription.unsubscribe();
    }
  }

    loadFriends(): void {
    this.usuarioService.getAmigos(this.userId).subscribe({
      next: (data) => {
        this.friends = data;
      },
      error: (error) => {
        console.error('Error cargando amigos:', error);
      }
    });
  }

  loadNotifications(): void {
    const id = this.userId.toString();
    this.notificationService.getNotificacionesUsuario(id).subscribe({
      next: (data) => {
        this.notifications = data;
      },
      error: (error) => {
        console.error('Error cargando notificaciones:', error);
      }
    });
  }

  eliminarAmigo(friendId: number, friendName: string): void {
    if (confirm(`¿Estás seguro de eliminar a ${friendName}?`)) {
      // 1. Eliminar el amigo
      this.usuarioService.eliminarAmigo(this.userId, friendId).subscribe({
        next: (response) => {
          console.log('Amigo eliminado:', response);
          
          // 2. Remover de la lista local
          this.friends = this.friends.filter(f => f.id !== friendId);
          
          // 3. PATRÓN OBSERVER: Enviar notificación al backend
          const notificacion = {
            destinatario: this.userId,
            mensaje: `Has eliminado a ${friendName} de tu lista de amigos`,
            tipo: 'friend_deleted'
          };

          console.log('Enviando notificación:', notificacion , "al usuario ID:", this.userId);
          
          this.notificationService.enviarNotificacion(notificacion).subscribe({
            next: (notifResponse) => {
              console.log('Notificación creada:', notifResponse);
              this.notificationService.emitNotificationRefresh();
              this.loadNotifications();
            },
            error: (error) => {
              console.error('Error creando notificación:', error);
            }
          });
          
          alert('Amigo eliminado correctamente');
        },
        error: (error) => {
          console.error('Error eliminando amigo:', error);
          alert('Error al eliminar amigo');
        }
      });
    }
  }

  marcarComoLeida(notificationId: number): void {
    this.notificationService.marcarComoLeida(notificationId).subscribe({
      next: () => {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
          notification.leida = true;
        }
      },
      error: (error) => {
        console.error('Error marcando notificación:', error);
      }
    });
  }

}
