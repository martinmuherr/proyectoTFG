# 🎓 Plataforma de Cursos con Tests, Pegatinas y Ranking

Este proyecto es una plataforma educativa donde profesores y alumnos pueden interactuar mediante cursos, tests, pegatinas y rankings.

## 🛠️ Requisitos

- Python 3.10+
- Node.js 18+
- npm o yarn
- Git

---

## 📁 Estructura del Proyecto

backend/
│ ├── authapp/
│ ├── cursos/
│ └── backend/ (configuración Django)
frontend/
│ └── frontend/
└── src/app/...


---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/tu-repo.git
cd tu-repo
```
### 2. Crear y activar el entorno virtual
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```
### 3. Instalar dependencias del backend y encender el servidor
```bash
pip install -r requirements.txt

pip install django djangorestframework djangorestframework-simplejwt pillow django-cors-headers
pip freeze > requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver

Backend disponible en http://localhost:8000
```
### 4. Ininiciar el frontend
```bash
cd frontend

cd frontend

npm install

ng serve

Frontend disponible en http://localhost:4200
```
🔐 Login
El login usa JWT (token almacenado en localStorage).

Rutas protegidas por token desde Angular con HttpInterceptor.

🧪 Características
Registro/Login de usuarios

Roles: profesor/alumno

Visualización y activación de tests

Resolución de preguntas con lógica de puntos y recompensas

Administración vía Django Admin

⚙️ Notas
Los cursos y tests solo los crea un administrador.

Puedes acceder a /admin con el superusuario.

Preguntas/respuestas se crean desde el panel admin.

