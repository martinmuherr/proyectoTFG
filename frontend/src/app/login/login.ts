import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  username = '';
  password = '';
  error = '';

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    this.error = '';
    this.http.post<any>('http://localhost:8000/api/auth/login/', {
      username: this.username,
      password: this.password
    }).subscribe({
      next: (res) => {
        localStorage.setItem('token', res.token); // Usa res.token
        localStorage.setItem('refresh_token', res.refresh);
        localStorage.setItem('role', res.role);
        this.router.navigate(['/cursos']);
      },
      error: (err) => { // Captura el error real
        console.error('Error en el login:', err); // Loguea el error
        this.error = 'Usuario o contraseña incorrectos'; // Mensaje genérico
      }
    });
  }

  goRegister() {
    this.router.navigate(['/register']);
  }
}
