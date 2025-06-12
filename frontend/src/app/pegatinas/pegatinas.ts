import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-pegatinas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pegatinas.html'
})
export class Pegatinas implements OnInit {
  pegatinas: any[] = [];
  error = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<any[]>('http://localhost:8000/api/mis-pegatinas/').subscribe({
      next: res => {
        this.pegatinas = res;
      },
      error: err => {
        this.error = 'No se pudieron cargar las pegatinas.';
        console.error(err);
      }
    });
  }
}
