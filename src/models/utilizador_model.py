from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.tarefa_model import TarefaModel



class UtilizadorModel(Base):
    __tablename__ = 'utilizadores'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    nome_utilizador: Mapped[str] = mapped_column(String(120), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(120))

    tarefas: Mapped[list["TarefaModel"]] = relationship(back_populates="utilizador", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self):
        return f'<UtilizadorModel(id={self.id}, nome={self.nome}, email={self.email})>'