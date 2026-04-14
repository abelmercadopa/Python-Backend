# Task Manager API

API REST desarrollada con Flask, SQLAlchemy, PostgreSQL y JWT.

## Características

- Registro e inicio de sesión con JWT.
- CRUD completo de tareas.
- Rutas protegidas por token.
- Endpoint con lógica de negocio:
  - `PATCH /tasks/<id>/complete`
  - `GET /tasks/summary`
- Proyecto listo para subir a GitHub.

## Estructura

```bash
task_manager_api/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   └── utils/
├── postman/
│   └── task_manager_api.postman_collection.json
├── .env.example
├── .gitignore
├── db_init.sql
├── requirements.txt
├── run.py
└── README.md
```

## Requisitos

- Python 3.11 o superior
- PostgreSQL instalado
- Git

## 1. Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Crear base de datos

Ejecuta en PostgreSQL:

```sql
CREATE DATABASE task_manager_db;
```

También puedes usar el archivo `db_init.sql`.

## 4. Configurar variables de entorno

Copia `.env.example` como `.env` y ajusta tus credenciales:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=super_secret_key_123
JWT_SECRET_KEY=jwt_super_secret_key_456
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_manager_db
```

## 5. Crear tablas con migraciones

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 6. Ejecutar proyecto

```bash
python run.py
```

La API quedará disponible en:

```bash
http://127.0.0.1:5000
```

## Endpoints

### Auth

- `POST /auth/register`
- `POST /auth/login`

### Tasks

- `GET /tasks`
- `GET /tasks/<id>`
- `POST /tasks`
- `PUT /tasks/<id>`
- `DELETE /tasks/<id>`
- `PATCH /tasks/<id>/complete`
- `GET /tasks/summary`

## Ejemplos de prueba

### Registrar usuario

`POST /auth/register`

```json
{
  "username": "abel",
  "email": "abel@gmail.com",
  "password": "123456"
}
```

### Login

`POST /auth/login`

```json
{
  "email": "abel@gmail.com",
  "password": "123456"
}
```

### Crear tarea

`POST /tasks`

Header:

```txt
Authorization: Bearer TU_TOKEN
```

Body:

```json
{
  "title": "Implementar API Flask",
  "description": "Terminar CRUD con JWT",
  "priority": "high",
  "due_date": "2026-04-20T18:00:00+00:00"
}
```

## Subir a GitHub

```bash
git init
git add .
git commit -m "Proyecto Flask REST API con JWT y PostgreSQL"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/task_manager_api.git
git push -u origin main
```

## Recomendación para la entrega

Incluye en tu repositorio:

- Código fuente
- `README.md`
- `.env.example`
- `requirements.txt`
- Colección Postman
- Capturas de pruebas en Postman o Thunder Client

