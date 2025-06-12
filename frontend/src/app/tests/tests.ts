import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-tests',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tests.html',
})
export class Tests implements OnInit {
  cursoId!: number;
  tests: any[] = [];
  error = '';

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.cursoId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadTests();
  }

  loadTests() {
    this.http.get<any[]>(`http://localhost:8000/api/cursos/${this.cursoId}/tests/`)
      .subscribe({
        next: (data) => this.tests = data.filter(t => t.active),
        error: () => this.error = 'No se pudieron cargar los tests'
      });
  }

  hacerTest(testId: number) {
    this.router.navigate(['/curso', this.cursoId, 'test', testId]);
  }
}
