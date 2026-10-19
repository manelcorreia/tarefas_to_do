import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from src.models.tarefa_model import Base
from src.repositories.tarefa_repositorio import TarefaRepositorio
from src.repositories.utilizador_repositorio import UtilizadorRepositorio


@pytest.fixture
def session():
    """Sessão ligada a uma BD SQLite em memória, nova para cada teste."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )


    @event.listens_for(engine, "connect")
    def _ativar_fks(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine)() as session:
        yield session
    engine.dispose()


@pytest.fixture
def repo(session):
    """Repositório já ligado à sessão de teste."""
    return TarefaRepositorio(session)

@pytest.fixture
def repo_utilizador(session):
    return UtilizadorRepositorio(session)