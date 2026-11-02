from fastapi import FastAPI
import uvicorn

from api.routers.tarefas import router as tarefas_router

app = FastAPI(
    title="API Gestão de Tarefas To-Do",
    description="API RESTFul construída com FastAPI, SQLAlchemy e Pydantic",
    version="1.0.0",
)

app.include_router(tarefas_router)

def root():
    return {
        "status": "online",
        "mensagem": "API a funcionar corretamente",
        "docs": "/docs",
    }

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)