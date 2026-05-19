import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { ServicioNotificacion } from '../../services/servicio-notificacion';

@Component({
  selector: 'app-header',
  standalone: false,
  templateUrl: './header.html',
  styleUrl: './header.css'
})
export class Header {
  notifications: any[] = [];
  private subscription!: Subscription;
  userId: number = 1;
  showNotifications = false;

  constructor(private notificationService: ServicioNotificacion) {}

  ngOnInit(): void {
    this.loadNotifications();

    // [OBSERVER - Observer 1] Header se suscribe al Subject: recibe el evento del Paso 11 y recarga notificaciones
    this.subscription = this.notificationService
      .onNotificationRefresh()
      .subscribe(() => {
        this.loadNotifications(); // GET /notificaciones/usuario/:id
      });
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  loadNotifications(): void {
  this.notificationService
    .getNotificacionesUsuario(this.userId.toString())
    .subscribe(data => {
      this.notifications = data;
    });
  }

  toggleNotifications(): void {
  this.showNotifications = !this.showNotifications;
  }
}
