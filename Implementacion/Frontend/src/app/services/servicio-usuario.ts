import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, take } from 'rxjs';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class ServicioUsuario {
  url= '/api'
  constructor(
    private httpClient: HttpClient,
    private router: Router
  ) { }

  register(dataRegister: any): Observable<any>{
    const body = {
      nombre: dataRegister.nombre,
      email: dataRegister.email,
      password: dataRegister.password,
      rol: 'user',
    };

    return this.httpClient.post(this.url + '/usuarios/register', body).pipe(take(1))
  }

  getAmigos(userId: number): Observable<any> {
    return this.httpClient.get<any>(`${this.url}/usuarios/amigos/${userId}`).pipe(take(1));
  }

  eliminarAmigo(userId: number, friendId: number): Observable<any> {
    let headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    const requestOptions = { headers: headers };
    return this.httpClient.delete<any>(`${this.url}/usuarios/${userId}/amigos/${friendId}`, requestOptions).pipe(take(1));
  }
}
