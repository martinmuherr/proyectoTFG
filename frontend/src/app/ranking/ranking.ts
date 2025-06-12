import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ranking',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ranking.html'
})
export class Ranking implements OnInit {
  cursoId!: number;
  ranking: any[] = [];
  error = '';

  constructor(private http: HttpClient, private route: ActivatedRoute) {}

  ngOnInit() {
    this.cursoId = Number(this.route.snapshot.paramMap.get('id'));
    this.cargarRanking();
  }

  cargarRanking() {
    this.http.get<any[]>(`http://localhost:8000/api/cursos/${this.cursoId}/ranking/`)
      .subscribe({
        next: data => this.ranking = data,
        error: err => {
          this.error = 'Error cargando ranking';
          console.error(err);
        }
      });
  }
}
