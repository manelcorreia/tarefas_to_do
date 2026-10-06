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

                nome, prioridade, concluida = linha_limpa.split(",")

                if concluida.strip().lower() == "true":
                    yield Tarefa(nome, int(prioridade), True)

                else:
                    yield Tarefa(nome, int(prioridade), False)