Cursos - REST API con Flask

Proyecto API REST desarrollado con Flask, usando Flask-Smorest para gestión de recursos,
JWT para autenticación y Docker para contenerización.

---

REQUISITOS

- Python 3.8+
- Docker y Docker Compose (opcional)
- pip (gestor de paquetes Python)

---

INSTALACIÓN Y EJECUCIÓN LOCAL

1. Crear y activar entorno virtual (PowerShell)

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

2. Instalar dependencias

    pip install flask flask-smorest flask-jwt-extended flask-migrate sqlalchemy passlib

3. Ejecutar la aplicación

    flask run

La API estará disponible en:  
http://localhost:5000

La documentación Swagger estará en:  
http://localhost:5000/docs

---

USO CON DOCKER

1. Construir imagen

    docker build -t rest-apis-flask-python .

2. Ejecutar con Docker Compose

    docker compose up --build --force-recreate --no-deps web

Esto levantará el contenedor y la API estará disponible en el puerto configurado (por defecto 5000).

---

MIGRACIONES CON FLASK-MIGRATE

Si usas migraciones para la base de datos, ejecutar:

    flask db init       (sólo la primera vez)
    flask db migrate -m "Mensaje descriptivo"
    flask db upgrade

---

NOTAS ADICIONALES

- Para reiniciar el servidor local después de cambios, presiona Ctrl+C y vuelve a ejecutar "flask run".
- Puedes configurar las siguientes variables de entorno para personalizar:

    DATABASE_URL      (ejemplo: sqlite:///data.db)
    JWT_SECRET_KEY    (clave secreta para JWT)

Para definirlas en PowerShell:

    setx DATABASE_URL "sqlite:///data.db"
    setx JWT_SECRET_KEY "clave_super_secreta"

Luego reinicia la consola para que tengan efecto.

- Para cambiar el puerto de Flask, ejecuta:

    flask run --port=5005

La documentación Swagger estará entonces en http://localhost:5005/docs

---

URLS ÚTILES

API Base:                 http://localhost:5000/
Documentación Swagger UI:  http://localhost:5000/docs

Si cambias el puerto, cambia el número en las URLs anteriores.


