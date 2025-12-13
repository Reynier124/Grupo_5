import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Register } from './pages/register/register'
import { MostrarAmigos } from './pages/mostrar-amigos/mostrar-amigos';

const routes: Routes = [
  {path : '', redirectTo: '/register', pathMatch: 'full'},
  {path: 'register', component: Register},
  {path: 'amigos/:id', component: MostrarAmigos},
  {path : '**', redirectTo: "/register"}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
