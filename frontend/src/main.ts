import { bootstrapApplication } from '@angular/platform-browser';
import { importProvidersFrom } from '@angular/core';
import { HttpClientModule, provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter, Routes } from '@angular/router';

import { App } from './app/app';
import { Login } from './app/login/login';
import { Register } from './app/register/register';
import { NotFound } from './app/not-found/not-found';
import { Cursos } from './app/cursos/cursos';
import { CursoDetalle } from './app/curso-detalle/curso-detalle';
//import { Tests } from './app/tests/tests';
import { TestResolver } from './app/test-resolver/test-resolver';
import { TestsList } from './app/test-list/test-list';
import { AuthInterceptor } from './app/interceptors/auth.interceptor';
import { Ranking } from './app/ranking/ranking';
import { Pegatinas } from './app/pegatinas/pegatinas';
import { Intercambio } from './app/intercambio/intercambio';
import { Perfil } from './app/perfil/perfil';

    const routes: Routes = [
      { path: '', component: Login },
      { path: 'register', component: Register },
      { path: 'cursos', component: Cursos },
      { path: 'curso/:id', component: CursoDetalle },
      //{ path: 'curso/:id/tests', component: Tests },
      { path: 'curso/:id/test/:testId', component: TestResolver },
      { path: 'curso/:cursoId/tests', component: TestsList },
      { path: 'curso/:id/ranking', component: Ranking },
      { path: 'curso/:id/pegatinas', component: Pegatinas },
      { path: 'curso/:id/intercambio', component: Intercambio },
      { path: 'curso/:id/perfil', component: Perfil },
      { path: '**', component: NotFound }
    ];

bootstrapApplication(App, {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([AuthInterceptor])),
  ]
});
