import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-intercambio',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './intercambio.html',
  styleUrls: ['./intercambio.css']
})
export class Intercambio implements OnInit {
  cursoId!: number;
  usuarios: any[] = [];
  pegatinasPropias: any[] = [];
  pegatinaSeleccionada: any = null;
  receptorId: number | null = null;
  pegatinaARecibirId: number | null = null;
  intercambiosPendientes: any[] = [];
  

  constructor(private http: HttpClient, private router: Router, private route: ActivatedRoute) {}

  ngOnInit() {
    const urlParams = this.router.url.split('/');
    this.cursoId = Number(this.route.snapshot.paramMap.get('cursoId'));

    this.cargarUsuarios();
    this.cargarPegatinas();
    this.cargarIntercambios();
  }

  cargarUsuarios() {
    this.http.get<any[]>('http://localhost:8000/api/cursos/usuarios-mismo-curso/')
      .subscribe(data => {
        this.usuarios = data;
      });
  }
  

  cargarPegatinas() {
    this.http.get<any[]>('http://localhost:8000/api/cursos/mis-pegatinas/').subscribe(data => {
      this.pegatinasPropias = data;
    });
  }

  cargarIntercambios() {
    this.http.get<any[]>('http://localhost:8000/api/cursos/intercambios/').subscribe(data => {
      this.intercambiosPendientes = data.filter(i => i.estado === 'pendiente');
    });
  }

  enviarSolicitud() {
    console.log('cursoId que se envía:', this.cursoId);  // Agrega esto
    if (!this.pegatinaSeleccionada || !this.receptorId || !this.cursoId) return;
  
    this.http.post('http://localhost:8000/api/cursos/intercambios/', {
      pegatina_emisor: this.pegatinaSeleccionada,
      receptor: this.receptorId,
      pegatina_receptor: null,
      curso: this.cursoId
    }).subscribe(() => {
      alert('Solicitud enviada');
      this.cargarIntercambios();
    });
  }
  
  
  aceptar(intercambio: any) {
    if (!this.pegatinaARecibirId) {
      alert('Debes elegir una pegatina tuya para intercambiar.');
      return;
    }
  
    this.http.patch(`http://localhost:8000/api/cursos/intercambios/${intercambio.id}/aceptar/`, {
      pegatina_receptor_id: this.pegatinaARecibirId
    }).subscribe(() => {
      alert('Intercambio realizado');
      this.cargarIntercambios(); 
      this.cargarPegatinas();
    });
  }
  
  rechazar(intercambio: any) {
    this.http.patch(`http://localhost:8000/api/cursos/intercambios/${intercambio.id}/rechazar/`, {})
      .subscribe(() => {
        alert('Intercambio rechazado');
        this.cargarIntercambios();
      });
  }

  volverAlCurso() {
    this.router.navigate(['/curso', this.cursoId]);
  }  
  
}
