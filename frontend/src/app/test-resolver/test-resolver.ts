import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-test-resolver',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './test-resolver.html',
})
export class TestResolver implements OnInit {
  cursoId!: number;
  testId!: number;
  test: any;
  preguntas: any[] = [];
  respuestasSeleccionadas: { [preguntaId: number]: number } = {};
  error = '';
  terminado = false;
  puntosObtenidos = 0;
  esProfesor = false;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    public router: Router
  ) {}

  ngOnInit() {
    this.cursoId = Number(this.route.snapshot.paramMap.get('id'));
    this.testId = Number(this.route.snapshot.paramMap.get('testId'));
    this.esProfesor = localStorage.getItem('role') === 'profesor';
    this.cargarTest();
  }

  cargarTest() {
    this.http.get<any>(`http://localhost:8000/api/cursos/${this.cursoId}/tests/${this.testId}/`)
      .subscribe({
        next: data => {
          this.test = data;
          this.preguntas = data.preguntas || [];
        },
        error: () => this.error = 'No se pudo cargar el test.'
      });
  }

  seleccionarRespuesta(preguntaId: number, respuestaId: number) {
    this.respuestasSeleccionadas[preguntaId] = respuestaId;
  }

  enviarRespuestas() {
    // Comprobamos que todas las preguntas tengan respuesta
    if (Object.keys(this.respuestasSeleccionadas).length !== this.preguntas.length) {
      this.error = 'Debes responder todas las preguntas.';
      return;
    }
    this.error = '';

    // Enviamos respuestas para validar y obtener puntos
    this.http.post<any>(`http://localhost:8000/api/cursos/${this.cursoId}/tests/${this.testId}/resolver/`, {
      respuestas: this.respuestasSeleccionadas
    }).subscribe({
      next: res => {
        this.terminado = true;
        this.puntosObtenidos = res.correctas || 0;
      },
      error: () => this.error = 'Error al enviar las respuestas.'
    });
  }
}
