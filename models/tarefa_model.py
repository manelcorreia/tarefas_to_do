from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TarefaModel(Base):
    __tablename__ = 'tarefas'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    prioridade: Mapped[int] = mapped_column()
    concluida: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'{self.nome} | {self.prioridade} | {self.concluida}'
