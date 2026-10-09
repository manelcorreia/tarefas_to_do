from sqlalchemy import select
from sqlalchemy.orm import Session
from models.tarefa_model import TarefaModel

class Repositorio:
    def __init__(self, session: Session):
        self.session = session

    def obter_por_nome(self, nome_tarefa: str) -> TarefaModel | None:
        comando = select(TarefaModel).where(TarefaModel.nome == nome_tarefa)
        tarefa = self.session.scalars(comando).one_or_none()
        return tarefa

    def nova_tarefa(self, nome_tarefa: str, prioridade_tarefa: int, concluida_tarefa: bool = False) -> bool:
        if self.obter_por_nome(nome_tarefa) is not None:
            return False
        tarefa = TarefaModel(nome=nome_tarefa,prioridade=prioridade_tarefa,concluida=concluida_tarefa)
        self.session.add(tarefa)
        return True

    def marcar_como_concluida(self, nome_tarefa: str) -> bool:
        tarefa = self.obter_por_nome(nome_tarefa)
        if tarefa is None or tarefa.concluida:
            return False
        tarefa.concluida = True
        return True

    def mudar_prioridade(self, nome_tarefa: str, nova_prioridade: int) -> bool:
        tarefa = self.obter_por_nome(nome_tarefa)
        if tarefa is None or tarefa.prioridade == nova_prioridade:
            return False
        tarefa.prioridade = nova_prioridade
        return True

    def ver_todas_tarefas(self) -> list[TarefaModel]:
        return list(self.session.scalars(select(TarefaModel)).all())

    def ver_tarefas_concluidas(self) -> list[TarefaModel]:
        comando = select(TarefaModel).where(TarefaModel.concluida).order_by(TarefaModel.prioridade.desc())
        tarefas = list(self.session.scalars(comando).all())
        return tarefas