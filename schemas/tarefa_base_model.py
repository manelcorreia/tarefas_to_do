from pydantic import BaseModel, Field, field_validator, ConfigDict

class TarefaBaseModel(BaseModel):
    nome: str = Field(min_length=4, max_length=150)
    prioridade: int = Field(ge=1, le=5)
    concluida: bool = Field(default=False)

    @field_validator('nome')
    @classmethod
    def validate_nome(cls, value: str) -> str:
        if any(l.isdigit() for l in value):
            raise ValueError("Nome não pode ter números")
        return value

class TarefaCreate(TarefaBaseModel):
    pass

class TarefaUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=4, max_length=150)
    prioridade: int | None = Field(default=None, ge=1, le=5)
    concluida: bool | None = Field(default=None)

class TarefaResponse(TarefaBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int