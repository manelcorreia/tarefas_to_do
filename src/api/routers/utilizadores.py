from fastapi import APIRouter, status, HTTPException

from schemas.login_request import LoginRequest
from schemas.utilizador_base_model import UtilizadorResponse, UtilizadorCreate, UtilizadorDetalhe, UtilizadorUpdate
from api.dependencies import UtilizadorServiceDep

router_utilizador = APIRouter(prefix="/utilizador", tags=["utilizador"])

@router_utilizador.post("/registo", response_model=UtilizadorResponse, status_code=status.HTTP_201_CREATED)
def registar_utilizador(dados: UtilizadorCreate, service: UtilizadorServiceDep):
    return service.fazer_registo(dados)

@router_utilizador.post("/login", response_model=UtilizadorResponse, status_code=status.HTTP_200_OK)
def fazer_login(credenciais: LoginRequest, service: UtilizadorServiceDep):
    utilizador = service.fazer_login(credenciais.email, credenciais.password)
    if not utilizador:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email ou password incorretos")
    return utilizador

@router_utilizador.get("/confirmacao/{utilizador_id}", response_model=bool, status_code=status.HTTP_200_OK)
def confirmar_alteracoes(utilizador_id: int, password: str, service: UtilizadorServiceDep):
    return service.confirmar_alteracoes(utilizador_id, password)

@router_utilizador.get("/detalhes/{utilizador_id}", response_model=UtilizadorDetalhe, status_code=status.HTTP_200_OK)
def ver_detalhes_utilizador(utilizador_id: int, service: UtilizadorServiceDep):
    return service.obter_perfil_com_detalhe(utilizador_id)

@router_utilizador.delete("/apagar/{utilizador_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_conta(utilizador_id: int, service: UtilizadorServiceDep):
    return service.apagar_conta(utilizador_id)

@router_utilizador.patch("/atualizar/{utilizador_id}", response_model=UtilizadorResponse, status_code=status.HTTP_200_OK)
def atualizar_dados_conta(dados: UtilizadorUpdate, utilizador_id: int, service: UtilizadorServiceDep):
    return service.atualizar_dados_do_utilizador(dados, utilizador_id)