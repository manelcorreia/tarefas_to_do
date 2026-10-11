import pytest

from models.tarefa_model import TarefaModel
from schemas.tarefa_base_model import TarefaCreate, TarefaUpdate


def test_nova_tarefa(repo, session):
    tarefa = repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False))

    assert tarefa.id is not None
    assert tarefa.nome == 'test'
    assert tarefa.prioridade == 1
    assert tarefa.concluida is False


def test_nova_tarefa_invalida(repo, session):
    with pytest.raises(ValueError):
        repo.nova_tarefa(TarefaCreate(nome='t3st', prioridade=1, concluida=False))

def test_atualizar_tarefa(repo, session):
    tarefa = repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False))

    assert tarefa.prioridade == 1

    repo.atualizar(tarefa.id, TarefaUpdate(prioridade=2))

    assert tarefa.prioridade == 2

def test_atualizar_tarefa_invalida(repo, session):
    tarefa = repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False))
    with pytest.raises(ValueError):
        repo.atualizar(tarefa.id, TarefaUpdate(prioridade=-2))

def test_remover_tarefa(repo, session):
    tarefa = repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False))

    sucesso = repo.remover(tarefa.id)

    assert sucesso is True

def test_remover_tarefa_invalida(repo, session):
    insucesso = repo.remover(1)

    assert insucesso is False

def test_listar_todas_tarefas(repo, session):
    repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False))
    repo.nova_tarefa(TarefaCreate(nome='teste', prioridade=2, concluida=False))

    tarefas = repo.ver_todas_tarefas()

    assert len(tarefas) == 2
    assert [(t.nome, t.prioridade, t.concluida) for t in tarefas] == [
        ("test", 1, False),
        ("teste", 2, False),
    ]
