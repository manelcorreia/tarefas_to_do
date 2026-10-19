import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.utilizador_model import UtilizadorModel


class TarefaModel(Base):
    __tablename__ = 'tarefas'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    prioridade: Mapped[int] = mapped_column()
    concluida: Mapped[bool] = mapped_column(default=False)
    data_registo: Mapped[datetime.date] = mapped_column(server_default=func.current_date())

    utilizador_id: Mapped[int] = mapped_column(ForeignKey('utilizadores.id', ondelete='CASCADE'))

    utilizador: Mapped["UtilizadorModel"] = relationship(back_populates="tarefas")

    def __repr__(self):
        return f'{self.nome} | {self.prioridade} | {self.concluida}'
