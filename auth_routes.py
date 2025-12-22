from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("")
async def autenticar():
    """"
    Rota padrão de pedidos . Todas precisam ser autenticadas
    """
    return {"mensagem": "Rota de autenticação!", "autenticado": False}