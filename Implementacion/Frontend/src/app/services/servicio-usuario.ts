import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
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
}
