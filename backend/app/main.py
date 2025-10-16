from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, admin
from contextlib import asynccontextmanager
from app.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("databses created")
    yield
    print("bye")


app = FastAPI(title="Clients API", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "hey bitch"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/greet/{name}")
def echo(name: str):
    return {"message": f"Hello!, {name}"}
