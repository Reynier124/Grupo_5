import { Injectable } from '@angular/core';
import { Observable, take, Subject } from 'rxjs';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class ServicioNotificacion {
  url='/api';
  // [OBSERVER - Subject] Canal central del patrón: almacena suscriptores y emite eventos hacia ellos
  private notificationSubject = new Subject<void>();

  constructor(
    private httpClient: HttpClient
  ) { }

  // READ - Obtener todas las notificaciones con filtros
  getNotificaciones(params: any): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    let httpParams = new HttpParams();
    Object.keys(params).forEach(key => {
      if (params[key]) {
        httpParams = httpParams.append(key, params[key]);
      }
    });
    const requestOptions = {headres: headers, params: httpParams};
    return this.httpClient.get<any>(`${this.url}/notificaciones`, requestOptions);
  }

  // READ - Obtener notificación por ID
  getNotificacionPorId(id: string): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    const requestOptions = {headers: headers};
    return this.httpClient.get<any>(`${this.url}/notificaciones/${id}`, requestOptions);
  }

  // CREATE - Crear una nueva notificación
  crearNotificacion(data: any): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    const requestOptions = {headers: headers};
    return this.httpClient.post<any>(`${this.url}/notificaciones`, data, requestOptions).pipe(take(1));
  }

  // UPDATE - Actualizar notificación
  actualizarNotificacion(id: string, data: any): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    const requestOptions = {headers: headers};
    return this.httpClient.put<any>(`${this.url}/notificaciones/${id}`, data, requestOptions).pipe(take(1));
  }

  // DELETE - Eliminar notificación
  eliminarNotificacion(id: string): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    const requestOptions = {headers: headers};
    return this.httpClient.delete<any>(`${this.url}/notificaciones/${id}`, requestOptions).pipe(take(1));
  }

  // [OBSERVER - Paso 3] ServicioNotificacion → NotificacionController: HTTP POST /notificaciones/enviar
  enviarNotificacion(data: any): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    const requestOptions = {headers: headers};
    return this.httpClient.post<any>(`${this.url}/notificaciones/enviar`, data, requestOptions).pipe(take(1));
  }

  // GET - Obtener notificaciones de amigos de un usuario
  getNotificacionesUsuario(id:string): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    const requestOptions = {headers: headers};
    return this.httpClient.get<any>(`${this.url}/notificaciones/usuario/${id}`, requestOptions).pipe(take(1));
  }

  // PUT - Marcar notificación como leída
  marcarComoLeida(id:number): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    const requestOptions = {headers: headers};
    return this.httpClient.put<any>(`${this.url}/notificaciones/marcar-leida/${id}`, requestOptions).pipe(take(1));
  }

  // [OBSERVER - Paso 11] Subject.next() notifica a todos los Observers suscriptos
  emitNotificationRefresh():void{
    this.notificationSubject.next();
  }

  // [OBSERVER] Expone el Observable para que los Observers (Header, MostrarAmigos) se suscriban
  onNotificationRefresh(): Observable<any> {
    return this.notificationSubject.asObservable();
  }

  getNotificationObservable(): Observable<any> {
    return this.notificationSubject.asObservable();
  }

}
