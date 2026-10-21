from sqlalchemy.orm import Session

from repositories.utilizador_repositorio import UtilizadorRepositorio
from schemas.utilizador_base_model import UtilizadorResponse, UtilizadorCreate, UtilizadorUpdate, UtilizadorDetalhe


class UtilizadorService:
    def __init__(self, session: Session, repositorio: UtilizadorRepositorio):
        self.session = session
        self.repositorio = repositorio

    def fazer_registo(self, dados: UtilizadorCreate) -> UtilizadorResponse | None:
        if self.repositorio.obter_por_email(dados.email):
            raise ValueError("Já existe um utilizador registado com esse email")

        if self.repositorio.obter_por_nome_utilizador(dados.nome_utilizador):
            raise ValueError("Já existe um utilizador registado com esse nome de utilizador")

        try:
            utilizador = self.repositorio.registar_utilizador(dados)

            self.session.commit()
            self.session.refresh(utilizador)
            return UtilizadorResponse.model_validate(utilizador)
        except Exception:
            self.session.rollback()
            raise

    def fazer_login(self, email: str, password: str) -> UtilizadorResponse | None:
        utilizador = self.repositorio.fazer_login(email, password)
        if utilizador:
            return UtilizadorResponse.model_validate(utilizador)
        return None

    def atualizar_dados_do_utilizador(self, dados: UtilizadorUpdate, utilizador_id: int) -> UtilizadorResponse:
        utilizador = self.repositorio.obter_utilizador_por_id(utilizador_id)
        if not utilizador:
            raise ValueError("Utilizador não encontrado")

        if dados.email is not None and dados.email != utilizador.email:
            if self.repositorio.obter_por_email(dados.email):
                raise ValueError("Já existe esse email registado noutra conta")

        try:
            utilizador_atualizado = self.repositorio.atualizar_dados_utilizador(dados, utilizador)
            self.session.commit()
            self.session.refresh(utilizador_atualizado)
            return UtilizadorResponse.model_validate(utilizador)
        except Exception:
            self.session.rollback()
            raise

    def confirmar_alteracoes(self, utilizador_id: int, password: str) -> bool:
        sucesso = self.repositorio.confirmar_com_password(utilizador_id, password)
        if sucesso:
            return True
        return False

    def apagar_conta(self, utilizador_id: int):
        utilizador = self.repositorio.obter_utilizador_por_id(utilizador_id)
        if not utilizador:
            raise ValueError("Utilizador não encontrado")

        try:
            utilizador_a_apagar = self.repositorio.apagar_utilizador(utilizador)
            if utilizador_a_apagar:
                self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def obter_perfil_com_detalhe(self, utilizador_id: int) -> UtilizadorDetalhe:
        utilizador = self.repositorio.obter_utilizador_por_id(utilizador_id)
        if not utilizador:
            raise ValueError("Utilizador não encontrado")

        try:
            return UtilizadorDetalhe.model_validate(utilizador)
        except Exception:
            raise