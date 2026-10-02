from typing import Generator

from models import Tarefa

class Leitor:
    def __init__(self, ficheiro: str):
        self.ficheiro = ficheiro

    def ler_ficheiro(self) -> Generator[Tarefa, None, None]:
        with open(self.ficheiro, "r", encoding="utf-8") as f:
            next(f, None)

            for linha in f:
                linha_limpa = linha.strip()
                if not linha_limpa:
                    continue

                coluna = linha_limpa.split(",")

                tarefa = Tarefa(coluna[0], int(coluna[1]))

                yield tarefa