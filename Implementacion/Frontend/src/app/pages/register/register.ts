import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from "@angular/router";
import { ServicioUsuario } from "../../services/servicio-usuario"


@Component({
  selector: 'app-register',
  standalone: false,
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class Register {
  userForm!: FormGroup;

  constructor(
    private formBuilder : FormBuilder,
    private servicioUsuario : ServicioUsuario,
  ){}

  ngOnInit(): void{
    this.userForm = this.formBuilder.group({
      nombre: ["", [Validators.required]],
      email : ["", [Validators.required, Validators.email]],
      password : ["", [Validators.required, Validators.minLength(4)]],
      confirmPassword : ["", [Validators.required]]
    }, {validator: this.passwordMatchValidator});
  }

  passwordMatchValidator(formGroup: FormGroup) {
    const password = formGroup.get('password')?.value;
    const confirmPassword = formGroup.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { mismatch: true };
  }

  irRegister(dataRegister: any) {
    console.log(dataRegister);
    this.servicioUsuario.register(dataRegister).subscribe({
      next: (rta: any) => {
        alert('Credenciales correctas!!!');
        console.log('Exito: ', rta);
        //this.router.navigateByUrl('home');
      },
      error: (err: any) => {
        alert('Usuario o contraseña incorrecta.');
        console.log('Error: ', err);
      },
      complete: () => {
        console.log('Finalizo');
      }
    });
  }

  submit() {
    console.log('Datos del formulario: ', this.userForm.value);
    if (this.userForm.valid) {
      console.log('Datos del formulario: ', this.userForm.value);
      console.log('Contraseña: '+this.userForm.value.password);
      this.irRegister(this.userForm.value);
    } else {
      this.markFormGroupTouched(this.userForm);
      alert('Por favor, corrija los errores en el formulario');
    }
  }

  private markFormGroupTouched(formGroup: FormGroup){
    (<any>Object).values(formGroup.controls).forEach((control:any) => {
      control.markAsTouched();
      if (control.controls){
        this.markFormGroupTouched(control)
      }
    })
  }

  showNameError(){
    return this.userForm.get('Nombre')?.invalid && this.userForm.get('Nombre')?.touched
  }

  showEmailError(){
    return this.userForm.get('email')?.invalid && this.userForm.get('email')?.touched
  }

  showPasswordError(){
    return this.userForm.get('password')?.invalid && this.userForm.get('password')?.touched
  }
  showConfirmPasswordError(){
    return this.userForm.get('confirmPassword')?.invalid && this.userForm.get('confirmPassword')?.touched
  }


}
