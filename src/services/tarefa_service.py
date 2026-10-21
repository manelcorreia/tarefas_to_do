from sqlalchemy.orm import Session

from repositories.tarefa_repositorio import TarefaRepositorio
from schemas.tarefa_base_model import TarefaCreate, TarefaResponse, TarefaUpdate


class TarefaService:
    def __init__(self, session: Session, repositorio: TarefaRepositorio):
        self.session = session
        self.repositorio = repositorio

    def adicionar_nova_tarefa(self, dados: TarefaCreate) -> TarefaResponse | None:
        if self.repositorio.obter_por_nome(dados.utilizador_id, dados.nome):
            raise ValueError("Já existe uma tarefa registada com esse nome")

        try:
            nova_tarefa = self.repositorio.nova_tarefa(dados)
            self.session.commit()
            self.session.refresh(nova_tarefa)
            schema = TarefaResponse.model_validate(nova_tarefa)
            return schema

        except Exception:
            self.session.rollback()
            raise

    def remover_tarefa(self, utilizador_id: int, tarefa_id: int):
        try:
            tarefa = self.repositorio.obter_por_id(utilizador_id, tarefa_id)
            if not tarefa:
                raise ValueError("Não existe tarefa com esse id")

            self.repositorio.remover(tarefa)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def atualizar_tarefa(self, utilizador_id: int, tarefa_id: int, dados: TarefaUpdate) -> TarefaResponse | None:
        try:
            tarefa = self.repositorio.obter_por_id(utilizador_id, tarefa_id)
            if not tarefa:
                raise ValueError("Não existe tarefa com esse id")

            if dados.nome is not None and dados.nome != tarefa.nome:
                if self.repositorio.obter_por_nome(utilizador_id, dados.nome):
                    raise ValueError("Já tens outra tarefa com esse nome")

            if dados.prioridade is not None and dados.prioridade == tarefa.prioridade:
                raise ValueError("A tarefa já tem essa prioridade")

            if dados.concluida is not None and dados.concluida == tarefa.concluida:
                if dados.concluida:
                    raise ValueError("A tarefa já está concluída")
                raise ValueError("A tarefa ainda não está concluída")

            schema = self.repositorio.atualizar(tarefa, dados)
            self.session.commit()
            self.session.refresh(schema)
            atualizada = TarefaResponse.model_validate(schema)
            return atualizada

        except Exception:
            self.session.rollback()
            raise

    def obter_tarefa_por_id(self, utilizador_id: int, tarefa_id: int):
        try:
            tarefa = self.repositorio.obter_por_id(utilizador_id, tarefa_id)
            if not tarefa:
                raise ValueError("Não existe tarefa com esse id")
        except Exception:
            raise

    def listar_todas_tarefas(self, utilizador_id: int) -> list[TarefaResponse]:
        tarefas = self.repositorio.ver_todas_tarefas(utilizador_id)
        return [TarefaResponse.model_validate(t) for t in tarefas]

    def listar_todas_tarefas_concluidas(self, utilizador_id: int) -> list[TarefaResponse]:
        tarefas = self.repositorio.ver_tarefas_concluidas(utilizador_id)
        return [TarefaResponse.model_validate(t) for t in tarefas]

    def listar_tarefas_x_prioridade(self, utilizador_id: int, prioridade: int) -> list[TarefaResponse]:
        tarefas = self.repositorio.ver_tarefas_de_x_prioridade(utilizador_id, prioridade)
        return [TarefaResponse.model_validate(t) for t in tarefas]

    def listar_tarefas_min_prioridade(self, utilizador_id: int, prioridade: int) -> list[TarefaResponse]:
        tarefas = self.repositorio.ver_tarefas_min_prioridade(utilizador_id, prioridade)
        return [TarefaResponse.model_validate(t) for t in tarefas]

    def listar_tarefas_max_prioridade(self, utilizador_id: int, prioridade: int) -> list[TarefaResponse]:
        tarefas = self.repositorio.ver_tarefas_max_prioridade(utilizador_id, prioridade)
        return [TarefaResponse.model_validate(t) for t in tarefas]