import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
@Component({
  selector: 'app-pegatinas',
  templateUrl: './pegatinas.html',
  styleUrls: ['./pegatinas.css'],
  standalone: true,
  imports: [CommonModule] 
})
export class Pegatinas implements OnInit {
  pegatinas: any[] = [];
  error = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<any[]>('http://localhost:8000/api/cursos/mis-pegatinas/')
      .subscribe({
        next: data => this.pegatinas = data,
        error: err => this.error = 'No se pudieron cargar las pegatinas.'
      });
  }
}