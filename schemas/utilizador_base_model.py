import string

from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict


class UtilizadorBaseModel(BaseModel):
    nome: str = Field(min_length=3, max_length=120)
    nome_utilizador: str = Field(min_length=3, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=120)

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        if any(l.isdigit() for l in valor):
            raise ValueError("Nome não pode ter números")
        return valor

    @field_validator('password')
    @classmethod
    def validar_password(cls, valor: str) -> str:
        tem_especial = any(l in string.punctuation for l in valor)
        tem_numero = any(l.isdigit() for l in valor)
        tem_maiuscula = any(l.isupper() for l in valor)

        if len(valor) < 8:
            raise ValueError("Password deve ter pelo menos 8 caracteres")

        if not tem_numero:
            raise ValueError("Password tem de ter pelo menos 1 número")

        if not tem_maiuscula:
            raise ValueError("Password tem de ter pelo menos 1 maiuscula")

        if not tem_especial:
            raise ValueError("Password tem de ter pelo menos 1 especial")

        return valor

class UtilizadorCreate(UtilizadorBaseModel):
    pass

class UtilizadorUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=120)
    nome_utilizador: str | None = Field(default=None, min_length=3, max_length=120)
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None, min_length=8, max_length=120)

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        if any(l.isdigit() for l in valor):
            raise ValueError("Nome não pode ter números")
        return valor

    @field_validator('password')
    @classmethod
    def validar_password(cls, valor: str) -> str:
        tem_especial = any(l in string.punctuation for l in valor)
        tem_numero = any(l.isdigit() for l in valor)
        tem_maiuscula = any(l.isupper() for l in valor)

        if len(valor) < 8:
            raise ValueError("Password deve ter pelo menos 8 caracteres")

        if not tem_numero:
            raise ValueError("Password tem de ter pelo menos 1 número")

        if not tem_maiuscula:
            raise ValueError("Password tem de ter pelo menos 1 maiuscula")

        if not tem_especial:
            raise ValueError("Password tem de ter pelo menos 1 especial")

        return valor

class UtilizadorResponse(UtilizadorBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int