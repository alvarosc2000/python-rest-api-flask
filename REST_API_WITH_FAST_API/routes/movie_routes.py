from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from datetime import datetime

from bd.database import Session
from models.movie import Movie as ModelMovie
from security.jwt_class import validateToken


# -----------------------------
# 📘 MODELOS Pydantic
# -----------------------------
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=3, max_length=60)
    overview: str = Field(..., min_length=15, max_length=250)
    year: int = Field(..., ge=1888, le=datetime.now().year)
    rating: float = Field(..., ge=0, le=10)
    category: str = Field(..., min_length=3, max_length=20)

    class Config:
        orm_mode = True


# -----------------------------
# 🔒 JWT AUTH
# -----------------------------
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data.get('email') != 'b@email.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')
        return data


# -----------------------------
# 🧠 RUTAS DE MOVIES
# -----------------------------
router = APIRouter(prefix="/movies", tags=["movies"])


# ✅ Obtener todas las películas
@router.get("/", dependencies=[Depends(BearerJWT())], status_code=200)
def get_movies():
    db = Session()
    try:
        data = db.query(ModelMovie).all()
        return JSONResponse(content=jsonable_encoder(data))
    finally:
        db.close()


# ✅ Obtener película por ID
@router.get("/{id}", status_code=200)
def get_movie_by_id(id: int = Path(ge=1)):
    db = Session()
    try:
        movie = db.query(ModelMovie).filter(ModelMovie.id == id).first()
        if not movie:
            raise HTTPException(status_code=404, detail='Película no encontrada')
        return JSONResponse(status_code=200, content=jsonable_encoder(movie))
    finally:
        db.close()


# ✅ Obtener películas por categoría
@router.get("/category/", status_code=200)
def get_movies_by_category(category: str):
    db = Session()
    try:
        data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
        if not data:
            raise HTTPException(status_code=404, detail='No hay películas en esa categoría')
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    finally:
        db.close()


# ✅ Crear nueva película
@router.post("/", status_code=201)
def create_movie(movie: Movie):
    db = Session()
    try:
        new_movie = ModelMovie(**movie.dict())
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        return JSONResponse(
            status_code=201,
            content={
                'message': 'Película creada correctamente',
                'movie': jsonable_encoder(new_movie)
            }
        )
    finally:
        db.close()


# ✅ Actualizar película existente
@router.put("/{id}", status_code=200)
def update_movie(id: int, movie: Movie):
    db = Session()
    try:
        movie_db = db.query(ModelMovie).filter(ModelMovie.id == id).first()
        if not movie_db:
            raise HTTPException(status_code=404, detail="Película no encontrada")

        for field, value in movie.dict().items():
            setattr(movie_db, field, value)

        db.commit()
        db.refresh(movie_db)

        return JSONResponse(
            content={
                "message": "Película actualizada correctamente",
                "movie": jsonable_encoder(movie_db)
            }
        )
    finally:
        db.close()


# ✅ Eliminar película
@router.delete("/{id}", status_code=200)
def delete_movie(id: int):
    db = Session()
    try:
        movie = db.query(ModelMovie).filter(ModelMovie.id == id).first()
        if not movie:
            raise HTTPException(status_code=404, detail=f'Película con id {id} no encontrada')

        db.delete(movie)
        db.commit()
        return JSONResponse(
            content={'message': f'Película con id {id} eliminada correctamente'}
        )
    finally:
        db.close()
