from sqlalchemy import select
from sqlalchemy.orm import Session
from models.tarefa_model import TarefaModel
from schemas.tarefa_base_model import TarefaCreate, TarefaUpdate


class Repositorio:
    def __init__(self, session: Session):
        self.session = session

    def obter_por_nome(self, nome_tarefa: str) -> TarefaModel | None:
        comando = select(TarefaModel).where(TarefaModel.nome == nome_tarefa)
        tarefa = self.session.scalars(comando).one_or_none()
        return tarefa

    def nova_tarefa(self, dados: TarefaCreate) -> TarefaModel:
        tarefa = TarefaModel(**dados.model_dump())
        self.session.add(tarefa)
        self.session.commit()
        self.session.refresh(tarefa)
        return tarefa

    def obter_por_id(self, tarefa_id: int) -> TarefaModel | None:
        return self.session.get(TarefaModel, tarefa_id)

    def atualizar(self, tarefa_id: int, dados: TarefaUpdate) -> TarefaModel | None:
        tarefa = self.obter_por_id(tarefa_id)
        if not tarefa:
            return None

        dados_atualizados = dados.model_dump(exclude_unset=True)

        for campo, valor in dados_atualizados.items():
            setattr(tarefa, campo, valor)

        self.session.commit()
        self.session.refresh(tarefa)
        return tarefa

    def remover(self, tarefa_id: int) -> bool:
        tarefa = self.obter_por_id(tarefa_id)
        if not tarefa:
            return False

        self.session.delete(tarefa)
        self.session.commit()
        return True

    def ver_todas_tarefas(self) -> list[TarefaModel]:
        return list(self.session.scalars(select(TarefaModel)).all())

    def ver_tarefas_concluidas(self) -> list[TarefaModel]:
        comando = select(TarefaModel).where(TarefaModel.concluida).order_by(TarefaModel.prioridade.desc())
        tarefas = list(self.session.scalars(comando).all())
        return tarefas