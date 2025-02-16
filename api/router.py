from fastapi import APIRouter


from api.routes import books
from api.routes import performance

api_router = APIRouter()
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(performance.router, tags=["performance"])
