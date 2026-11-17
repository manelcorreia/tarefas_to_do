from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import JSONResponse

from api.exceptions import NaoExisteTarefaComID, JaExisteTarefaComNome, TarefaJaTemEssaPrioridade, TarefaNaoConcluida, \
    TarefaJaConcluida, EmailJaEmUso, NomeUtilizadorJaEmUso, UtilizadorNaoEncontrado
from api.routers.tarefas import router as tarefas_router
from api.routers.utilizadores import router_utilizador as utilizadores_router

app = FastAPI(
    title="API Gestão de Tarefas To-Do",
    description="API RESTFul construída com FastAPI, SQLAlchemy e Pydantic",
    version="1.0.0",
)

app.include_router(tarefas_router)
app.include_router(utilizadores_router)

@app.exception_handler(NaoExisteTarefaComID)
def nao_existe_tarefa_com_id(request: Request, exc: NaoExisteTarefaComID):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(JaExisteTarefaComNome)
def ja_existe_tarefa_com_nome(request: Request, exc: JaExisteTarefaComNome):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(TarefaJaTemEssaPrioridade)
def tarefa_ja_tem_essa_prioridade(request: Request, exc: TarefaJaTemEssaPrioridade):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(TarefaNaoConcluida)
def tarefa_ainda_nao_esta_concluida(request: Request, exc: TarefaNaoConcluida):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(TarefaJaConcluida)
def tarefa_ja_concluida(request: Request, exc: TarefaJaConcluida):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(EmailJaEmUso)
def email_ja_registado(request: Request, exc: EmailJaEmUso):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(NomeUtilizadorJaEmUso)
def nome_utilizador_ja_registado(request: Request, exc: NomeUtilizadorJaEmUso):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(UtilizadorNaoEncontrado)
def utilizador_nao_encontrado(request: Request, exc: UtilizadorNaoEncontrado):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.get("/")
def root():
    return {
        "status": "online",
        "mensagem": "API a funcionar corretamente",
        "docs": "/docs",
    }

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)