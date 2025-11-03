from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas.user_schema import User
from security.jwt_class import createToken

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
def login(user: User):
    token = createToken(user.dict())
    return JSONResponse(content={"token": token})
