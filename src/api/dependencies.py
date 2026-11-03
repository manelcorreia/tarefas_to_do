from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from core.engine import SessionLocal
from repositories.tarefa_repositorio import TarefaRepositorio
from repositories.utilizador_repositorio import UtilizadorRepositorio
from services.tarefa_service import TarefaService
from services.utilizador_service import UtilizadorService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]

def get_tarefa_service(db: DbSession) -> TarefaService:
    repo = TarefaRepositorio(db)
    return TarefaService(db, repo)

TarefaServiceDep = Annotated[TarefaService, Depends(get_tarefa_service)]

def get_utilizador_service(db: DbSession) -> UtilizadorService:
    repo = UtilizadorRepositorio(db)
    return UtilizadorService(db, repo)

UtilizadorServiceDep = Annotated[UtilizadorService, Depends(get_utilizador_service)]