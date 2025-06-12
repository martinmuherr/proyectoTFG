import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-curso-detalle',
  templateUrl: './curso-detalle.html',
  standalone: true,
})
export class CursoDetalle implements OnInit {
  curso: any;
  cursoId!: number;

  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.cursoId = Number(this.route.snapshot.paramMap.get('id'));
    this.http.get(`http://localhost:8000/api/cursos/${this.cursoId}/`).subscribe({
      next: data => this.curso = data,
      error: err => console.error('Error al cargar curso', err)
    });
  }

  verTests() {
  this.router.navigate(['/curso', this.cursoId, 'tests']);
}

}
