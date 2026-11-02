from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from api.dependencies import TarefaServiceDep
from schemas.tarefa_base_model import TarefaResponse, TarefaCreate, TarefaUpdate

router = APIRouter(prefix="/tarefas", tags=["tarefas"])

@router.post("", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def create_tarefas(tarefa: TarefaCreate, service: TarefaServiceDep):
    return service.adicionar_nova_tarefa(tarefa)

@router.get("", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def lista_tarefas(
        utilizador_id: int,
        service: TarefaServiceDep,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_todas_tarefas(utilizador_id)

@router.get("/concluidas", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas_concluidas(
        utilizador_id: int,
        service: TarefaServiceDep,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_todas_tarefas_concluidas(utilizador_id)

@router.get("/prioridade/{prioridade}", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas_x_prioridades(
        utilizador_id: int,
        service: TarefaServiceDep,
        prioridade: int,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_tarefas_x_prioridade(utilizador_id, prioridade)

@router.get("/prioridade/{prioridade}/max", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas_menor_que_prioridade(
        utilizador_id: int,
        service: TarefaServiceDep,
        prioridade: int,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_tarefas_max_prioridade(utilizador_id, prioridade)

@router.get("/prioridade/{prioridade}/min", response_model=list[TarefaResponse], status_code=status.HTTP_200_OK)
def listar_tarefas_maior_que_prioridade(
        utilizador_id: int,
        service: TarefaServiceDep,
        prioridade: int,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=0, le=20)] = 5,
):
    return service.listar_tarefas_min_prioridade(utilizador_id, prioridade)

@router.get("/{tarefa_id}", response_model=TarefaResponse, status_code=status.HTTP_200_OK)
def obter_tarefa(tarefa_id: int, utilizador_id: int, service: TarefaServiceDep):
    try:
        return service.obter_tarefa_por_id(utilizador_id, tarefa_id) #[cite: 8]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tarefa(utilizador_id: int, tarefa_id: int, service: TarefaServiceDep):
    return service.remover_tarefa(utilizador_id, tarefa_id)

@router.patch("/{tarefa_id}", response_model=TarefaResponse, status_code=status.HTTP_200_OK)
def atualizar_tarefa(utilizador_id: int, tarefa_id: int, tarefa: TarefaUpdate, service: TarefaServiceDep):
    return service.atualizar_tarefa(utilizador_id, tarefa_id, tarefa)