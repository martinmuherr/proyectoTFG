import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './perfil.html',
  styleUrls: ['./perfil.css']
})
export class Perfil implements OnInit {
  usuario: any = {};
  intercambios: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get('http://localhost:8000/api/auth/profile/').subscribe(data => {
      this.usuario = data;
      if (this.usuario.role === 'profesor') {
        this.cargarHistorial();
      }
    });
  }
  
  cargarHistorial() {
    this.http.get<any[]>('http://localhost:8000/api/cursos/historial-intercambios/')
      .subscribe(data => {
        this.intercambios = data;
      });
  }
  
}
