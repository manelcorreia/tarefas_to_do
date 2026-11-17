class JaExisteTarefaComNome(Exception):
    pass

class NaoExisteTarefaComID(Exception):
    pass

class TarefaJaTemEssaPrioridade(Exception):
    pass

class TarefaJaConcluida(Exception):
    pass

class TarefaNaoConcluida(Exception):
    pass

class EmailJaEmUso(Exception):
    pass

class NomeUtilizadorJaEmUso(Exception):
    pass

class UtilizadorNaoEncontrado(Exception):
    pass