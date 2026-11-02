from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from schemas.tarefa_base_model import TarefaResponse, TarefaCreate, TarefaUpdate
from services.tarefa_service import TarefaService

router = APIRouter(prefix="/tarefas", tags=["tarefas"])

@router.post("", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def create_tarefas(tarefa: TarefaCreate, service: TarefaService):
    return service.adicionar_nova_tarefa(tarefa)

@router.get("", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def lista_tarefas(
        utilizador_id: int,
        service: TarefaService,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_todas_tarefas(utilizador_id)

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_tarefa(utilizador_id: int, tarefa_id: int, service: TarefaService):
    return service.remover_tarefa(utilizador_id, tarefa_id)

@router.patch("", response_model=TarefaResponse, status_code=status.HTTP_200_OK)
def atualizar_tarefa(utilizador_id: int, tarefa_id: int, tarefa: TarefaUpdate, service: TarefaService):
    return service.atualizar_tarefa(utilizador_id, tarefa_id, tarefa)

@router.get("", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas_concluidas(
        utilizador_id: int,
        service: TarefaService,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_todas_tarefas_concluidas(utilizador_id)

@router.get("/prioridade/{prioridade}", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas_x_prioridades(
        utilizador_id: int,
        service: TarefaService,
        prioridade: int,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_tarefas_x_prioridade(utilizador_id, prioridade)

@router.get("/prioridade/<{prioridade}", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas_menor_que_prioridade(
        utilizador_id: int,
        service: TarefaService,
        prioridade: int,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_tarefas_max_prioridade(utilizador_id, prioridade)

@router.get("/prioridade/>{prioridade}", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas_maior_que_prioridade(
        utilizador_id: int,
        service: TarefaService,
        prioridade: int,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_tarefas_min_prioridade(utilizador_id, prioridade)