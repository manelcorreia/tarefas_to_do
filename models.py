from dataclasses import dataclass

@dataclass
class Tarefa:
    nome: str
    prioridade: int
    concluida: bool = False