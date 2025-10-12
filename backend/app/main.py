from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Clients API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healt")
def health():
    return {"status": "healthy"}


@app.get("/greet/{name}")
def echo(name: str):
    return {"message": f"Hello!, {name}"}
