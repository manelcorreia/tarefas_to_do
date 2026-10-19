from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.tarefa_model import TarefaModel
from src.schemas.tarefa_base_model import TarefaCreate, TarefaUpdate

class TarefaRepositorio:
    def __init__(self, session: Session):
        self.session = session

    def obter_por_nome(self, utilizador_id: int, nome_tarefa: str) -> TarefaModel | None:
        """obter tarefa pelo nome"""
        comando = (select(
            TarefaModel
        ).where(TarefaModel.utilizador_id == utilizador_id, TarefaModel.nome == nome_tarefa))

        tarefa = self.session.scalars(comando).one_or_none()
        return tarefa

    def nova_tarefa(self, dados: TarefaCreate) -> TarefaModel:
        """criar uma nova tarefa"""
        tarefa = TarefaModel(**dados.model_dump())
        self.session.add(tarefa)
        self.session.commit()
        self.session.refresh(tarefa)
        return tarefa

    def obter_por_id(self, utilizador_id: int,tarefa_id: int) -> TarefaModel | None:
        """obter tarefa pelo id"""
        comando = select(TarefaModel).where(TarefaModel.utilizador_id == utilizador_id, TarefaModel.id == tarefa_id)
        return self.session.scalars(comando).one_or_none()

    def atualizar(self, utilizador_id: int , tarefa_id: int, dados: TarefaUpdate) -> TarefaModel | None:
        """atualizar tarefa pelo id"""
        tarefa = self.obter_por_id(utilizador_id, tarefa_id)
        if not tarefa:
            return None

        dados_atualizados = dados.model_dump(exclude_unset=True)

        for campo, valor in dados_atualizados.items():
            setattr(tarefa, campo, valor)

        self.session.commit()
        self.session.refresh(tarefa)
        return tarefa

    def remover(self, utilizador_id: int,tarefa_id: int) -> bool:
        """remover tarefa pelo id"""
        tarefa = self.obter_por_id(utilizador_id, tarefa_id)
        if not tarefa:
            return False

        self.session.delete(tarefa)
        self.session.commit()
        return True

    def ver_todas_tarefas(self, utilizador_id: int) -> list[TarefaModel]:
        """ver todas as tarefas registadas na base de dados"""
        return list(self.session.scalars(select(TarefaModel).where(TarefaModel.utilizador_id == utilizador_id)).all())

    def ver_tarefas_concluidas(self, utilizador_id: int) -> list[TarefaModel]:
        """ver todas as tarefas concluídas registadas na base de dados"""
        comando = select(TarefaModel).where(TarefaModel.concluida, TarefaModel.utilizador_id == utilizador_id).order_by(TarefaModel.prioridade.desc())
        tarefas = list(self.session.scalars(comando).all())
        return tarefas

    def ver_tarefas_de_x_prioridade(self, utilizador_id: int, prioridade: int) -> list[TarefaModel]:
        """ver todas as tarefas com prioridade igual à pedida"""
        comando = select(TarefaModel).where(TarefaModel.prioridade == prioridade, TarefaModel.utilizador_id == utilizador_id)
        return list(self.session.scalars(comando).all())

    def ver_tarefas_min_prioridade(self, utilizador_id: int, prioridade: int) -> list[TarefaModel]:
        """ver todas as tarefas com prioridade mínima igual à pedida"""
        comando = select(TarefaModel).where(TarefaModel.prioridade >= prioridade, TarefaModel.utilizador_id == utilizador_id)
        return list(self.session.scalars(comando).all())

    def ver_tarefas_max_prioridade(self, utilizador_id: int, prioridade: int) -> list[TarefaModel]:
        """ver todas as tarefas com prioridade máxima igual à pedida"""
        comando = select(TarefaModel).where(TarefaModel.prioridade <= prioridade, TarefaModel.utilizador_id == utilizador_id)
        return list(self.session.scalars(comando).all())