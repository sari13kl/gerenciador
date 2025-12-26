from fastapi import APIRouter, Depends
from schemas import PedidoSchema
from dependencies import pegar_sessao
from sqlalchemy.orm import sessionmaker
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["[pedidos]"])

@order_router.get("")
async def pedidos():
    return {"mensagem": "Rota de pedidos!"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: sessionmaker = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.user_id)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}