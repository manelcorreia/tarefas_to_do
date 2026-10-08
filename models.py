from dataclasses import dataclass

@dataclass
class Tarefa:
    nome: str
    prioridade: int
    concluida: bool = False

    def __repr__(self):
        return f'{self.nome} {self.prioridade} {self.concluida}'