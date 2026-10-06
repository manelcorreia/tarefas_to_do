from typing import Iterable

from models import Tarefa


class Exportador:
    def guardar_dados(self, objetos: Iterable[Tarefa], ficheiro: str) -> None:
        with open(ficheiro, 'w', encoding='utf-8') as f:
            f.write("nome,prioridade,concluida\n")
            for objeto in objetos:
                linha = f"{objeto.nome},{objeto.prioridade},{objeto.concluida}\n"
                f.write(linha)

    def ficheiro_tarefas_concluidas(self, objetos: Iterable[Tarefa], ficheiro: str) -> None:
        with open(ficheiro, 'a', encoding='utf-8') as f:
            f.write("nome,prioridade,concluida\n")
            for objeto in objetos:
                if objeto.concluida:
                    linha = f"{objeto.nome},{objeto.prioridade},{objeto.concluida}\n"
                    f.write(linha)