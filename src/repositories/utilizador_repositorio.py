from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.utilizador_model import UtilizadorModel
from src.schemas.utilizador_base_model import UtilizadorCreate, UtilizadorUpdate


class UtilizadorRepositorio:
    def __init__(self, session: Session):
        self.session = session

    def registar_utilizador(self, dados: UtilizadorCreate) -> UtilizadorModel:
        """registar novo utilizador"""
        novo_utilizador = UtilizadorModel(**dados.model_dump())
        self.session.add(novo_utilizador)
        return novo_utilizador

    def obter_por_nome_utilizador(self, nome_utilizador: str) -> UtilizadorModel:
        """obter utilizador por nome utilizador"""
        comando = select(UtilizadorModel).where(UtilizadorModel.nome_utilizador == nome_utilizador)
        utilizador = self.session.scalars(comando).one_or_none()
        return utilizador

    def obter_por_email(self, email_utilizador: str) -> UtilizadorModel:
        """obter utilizador por email"""
        comando = select(UtilizadorModel).where(UtilizadorModel.email == email_utilizador)
        utilizador = self.session.scalars(comando).one_or_none()
        return utilizador

    def atualizar_dados_utilizador(self, dados: UtilizadorUpdate, utilizador: UtilizadorModel) -> UtilizadorModel:
        """atualizar dados utilizador"""
        dados_utilizador = dados.model_dump(exclude_unset=True)

        for campo, valor in dados_utilizador.items():
            setattr(utilizador, campo, valor)

        return utilizador

    def apagar_utilizador(self, utilizador: UtilizadorModel) -> bool:
        """apagar utilizador"""
        if not utilizador:
            return False
        self.session.delete(utilizador)
        return True

    def fazer_login(self, email: str, password: str) -> UtilizadorModel | None:
        """fazer login"""
        comando = select(UtilizadorModel).where(UtilizadorModel.email == email, UtilizadorModel.password == password)
        utilizador = self.session.scalars(comando).one_or_none()
        if utilizador is not None:
            return utilizador
        return None

    def confirmar_com_password(self, utilizador_id: int, password: str) -> bool:
        """confirmar qualquer ação através da password"""
        comando = select(UtilizadorModel).where(UtilizadorModel.id == utilizador_id, UtilizadorModel.password == password)
        utilizador = self.session.scalars(comando).one_or_none()
        if utilizador:
            return True
        return False

    def obter_utilizador_por_id(self, utilizador_id: int) -> UtilizadorModel | None:
        """obter utilizador por id"""
        utilizador = self.session.get(UtilizadorModel, utilizador_id)
        return utilizador