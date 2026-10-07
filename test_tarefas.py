import pytest

from models import Tarefa
from repositorio import Repositorio


@pytest.fixture
def repo():
    return Repositorio()

@pytest.fixture
def tarefa_exemplo():
    return Tarefa(nome="Estudar Pydantic", prioridade=1)

def test_criacao_tarefa_exemplo(tarefa_exemplo):
    assert tarefa_exemplo.nome == "Estudar Pydantic"
    assert tarefa_exemplo.prioridade == 1
    assert tarefa_exemplo.concluida is False

def test_lista_tarefas(repo):
    assert repo.nova_tarefa("Estudar",1) == True

    assert len(repo.tarefas) == 1

def test_obter_tarefa_por_nome(repo):
    repo.nova_tarefa("Estudar", 1)

    tarefa = repo.obter_por_nome("Estudar")
    assert tarefa is not None
    assert tarefa == repo.tarefas[0]

def test_mudar_nivel_prioridade(repo, tarefa_exemplo):
    repo.tarefas.append(tarefa_exemplo)
    assert tarefa_exemplo.prioridade == 1
    sucesso = repo.mudar_prioridade("Estudar Pydantic",2)
    assert sucesso is True
    assert tarefa_exemplo.prioridade == 2

def test_marcar_como_concluida(repo, tarefa_exemplo):
    repo.tarefas.append(tarefa_exemplo)
    assert tarefa_exemplo.concluida is False
    sucesso = repo.marcar_como_concluida("Estudar Pydantic")
    assert sucesso is True
    assert tarefa_exemplo.concluida is True