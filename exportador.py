from typing import Iterable

from models import Tarefa


class Exportador:
    @staticmethod
    def guardar_dados(objetos: Iterable[Tarefa], ficheiro: str = "tarefas_to_do.csv") -> None:
        with open(ficheiro, 'a', encoding='utf-8') as f:
            for objeto in objetos:
                linha = f"{objeto.nome},{objeto.prioridade},{objeto.concluida}\n"
                f.write(linha)

    @staticmethod
    def ficheiro_tarefas_concluidas(objetos: Iterable[Tarefa], ficheiro: str = "tarefas_concluidas.csv") -> None:
        with open(ficheiro, 'a', encoding='utf-8') as f:
            for objeto in objetos:
                if objeto.concluida:
                    linha = f"{objeto.nome},{objeto.prioridade},{objeto.concluida}\n"
                    f.write(linha)