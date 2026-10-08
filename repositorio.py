from typing import Generator, Iterable

from models import Tarefa


class Repositorio:
    def __init__(self, tarefas: list[Tarefa] | None = None):
        self.tarefas = tarefas if tarefas is not None else []

    def obter_por_nome(self, nome_tarefa: str) -> Tarefa | None:
        for tarefa in self.tarefas:
            if tarefa.nome == nome_tarefa:
                return tarefa
        return None

    def nova_tarefa(self, nome_tarefa: str, prioridade_tarefa: int, concluida_tarefa: bool = False) -> bool:
        if self.obter_por_nome(nome_tarefa) is not None:
            return False
        self.tarefas.append(Tarefa(nome_tarefa, prioridade_tarefa, concluida_tarefa))
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