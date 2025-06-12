import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cursos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cursos.html'
})
export class Cursos {
  cursos: any[] = [];
  error = '';

  constructor(private http: HttpClient, private router: Router) {
    this.loadCursos();
  }

  loadCursos() {
    this.http.get<any[]>('http://localhost:8000/api/cursos/')
      .subscribe({
        next: data => this.cursos = data,
        error: () => this.error = 'No se pudieron cargar los cursos'
      });
  }

  unirse(cursoId: number) {
    this.router.navigate(['/curso', cursoId]);
  }
}
