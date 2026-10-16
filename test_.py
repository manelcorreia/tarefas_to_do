import pytest
from pydantic import ValidationError

from schemas.tarefa_base_model import TarefaCreate, TarefaUpdate, TarefaResponse
from schemas.utilizador_base_model import UtilizadorCreate, UtilizadorUpdate


def test_nova_tarefa(repo, repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test',nome_utilizador="test123",email="test@gmail.com",password="Test123#"))
    tarefa = repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False, utilizador_id=utilizador.id))

    assert tarefa.id is not None
    assert tarefa.nome == 'test'
    assert tarefa.prioridade == 1
    assert tarefa.concluida is False
    assert tarefa.utilizador_id == utilizador.id


def test_nova_tarefa_invalida(repo, repo_utilizador, session):
    with pytest.raises(ValueError):
        utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))
        repo.nova_tarefa(TarefaCreate(nome='t3st', prioridade=1, concluida=False, utilizador_id=utilizador.id))

def test_atualizar_tarefa(repo, repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test',nome_utilizador="test123",email="test@gmail.com",password="Test123#"))
    tarefa = repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False, utilizador_id=utilizador.id))

    assert tarefa.prioridade == 1

    repo.atualizar(tarefa_id=tarefa.id, utilizador_id=utilizador.id, dados=TarefaUpdate(prioridade=2))

    assert tarefa.prioridade == 2

def test_atualizar_tarefa_invalida(repo, repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test',nome_utilizador="test123",email="test@gmail.com",password="Test123#"))
    tarefa = repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False, utilizador_id=utilizador.id))
    with pytest.raises(ValueError):
        repo.atualizar(tarefa.id, TarefaUpdate(prioridade=-2))

def test_remover_tarefa(repo, repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test',nome_utilizador="test123",email="test@gmail.com",password="Test123#"))
    tarefa = repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False, utilizador_id=utilizador.id))

    sucesso = repo.remover(tarefa_id=tarefa.id, utilizador_id=utilizador.id)

    assert sucesso is True

def test_remover_tarefa_invalida(repo, repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test',nome_utilizador="test123",email="test@gmail.com",password="Test123#"))

    insucesso = repo.remover(tarefa_id=1, utilizador_id=utilizador.id)

    assert insucesso is False

def test_listar_todas_tarefas(repo, repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test',nome_utilizador="test123",email="test@gmail.com",password="Test123#"))
    repo.nova_tarefa(TarefaCreate(nome='test', prioridade=1, concluida=False, utilizador_id=utilizador.id))
    repo.nova_tarefa(TarefaCreate(nome='teste', prioridade=2, concluida=False, utilizador_id=utilizador.id))

    tarefas = repo.ver_todas_tarefas(utilizador_id=utilizador.id)

    assert len(tarefas) == 2
    assert [(t.nome, t.prioridade, t.concluida) for t in tarefas] == [
        ("test", 1, False),
        ("teste", 2, False),
    ]

def test_registar_utilizador(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test',nome_utilizador="test123",email="test@gmail.com",password="Test123#"))

    assert utilizador is not None
    assert utilizador.nome == 'test'
    assert utilizador.email == 'test@gmail.com'
    assert utilizador.password == 'Test123#'
    assert utilizador.nome_utilizador == 'test123'

def test_registar_dados_invalidos(repo_utilizador, session):
    with pytest.raises(ValidationError):
        repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test3', nome_utilizador="test123", email="testgmail.com", password="Test123#"))

def test_obter_utilizador_por_nome_utilizador(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test',nome_utilizador="test123",email="test@gmail.com",password="Test123#"))

    assert repo_utilizador.obter_por_nome_utilizador("test123") == utilizador

def test_obter_utilizador_por_email(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))

    assert repo_utilizador.obter_por_email("test@gmail.com") == utilizador

def test_atualizar_utilizador_dados_completos(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))

    schema = UtilizadorUpdate(nome='teste', nome_utilizador="test1234", email="teste@gmail.com", password="Test143#")

    repo_utilizador.atualizar_dados_utilizador(schema, utilizador)

    assert utilizador.nome_utilizador == "test1234"
    assert utilizador.nome == "teste"
    assert utilizador.email == "teste@gmail.com"
    assert utilizador.password == "Test143#"

def test_atualizar_utilizador_dados_incompletos(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))

    schema = UtilizadorUpdate(nome='teste')

    repo_utilizador.atualizar_dados_utilizador(schema, utilizador)

    assert utilizador.nome == "teste"
    assert schema.model_dump() == {"nome":"teste", "nome_utilizador":None, "email":None, "password":None}

def test_apagar_utilizador(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))

    assert repo_utilizador.apagar_utilizador(utilizador) is True

def test_apagar_utilizador_inexistente(repo_utilizador, session):
    assert repo_utilizador.apagar_utilizador(None) is False

def test_fazer_login_sucesso(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))

    assert repo_utilizador.fazer_login(utilizador.email, utilizador.password) == utilizador

def test_fazer_login_fail(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))

    assert repo_utilizador.fazer_login(utilizador.email, "Tjgfmg34#") is None

def test_confirmar_atraves_password(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))

    assert repo_utilizador.confirmar_com_password(utilizador.id, utilizador.password) is True

def test_confirmar_atraves_password_invalida(repo_utilizador, session):
    utilizador = repo_utilizador.registar_utilizador(UtilizadorCreate(nome='test', nome_utilizador="test123", email="test@gmail.com", password="Test123#"))

    assert repo_utilizador.confirmar_com_password(utilizador.id, "fsdogT754873$") is False