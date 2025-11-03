from fastapi import FastAPI
from bd.database import Base, engine
from routes.movie_routes import router as movie_router
from routes.auth_routes import router as auth_router  # si lo tienes

app = FastAPI(
    title='FastAPI REST API',
    description='Curso de FastAPI con JWT y SQLAlchemy',
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# Montamos las rutas
app.include_router(auth_router)
app.include_router(movie_router)

@app.get("/", tags=["inicio"])
def home():
    return {"message": "Bienvenido a la API de películas 🎬"}
