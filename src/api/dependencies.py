from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from core.engine import SessionLocal
from repositories.tarefa_repositorio import TarefaRepositorio
from services.tarefa_service import TarefaService


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