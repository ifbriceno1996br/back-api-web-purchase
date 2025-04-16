from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import SessionLocal
from app.initial_data import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir el router de la API
app.include_router(api_router, prefix=settings.API_V1_STR)

# @app.on_event("startup")
# async def startup_event():
#     db = SessionLocal()
#     init_db(db)
#     db.close()

@app.get("/")
def root():
    return {"message": "Welcome to Purchase Request API"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
