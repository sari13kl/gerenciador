from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from dependencies import pegar_sessao, verificar_token
from sqlalchemy.orm import sessionmaker
from models import Pedido, User, ItemPedido
from typing import List

order_router = APIRouter(prefix="/pedidos", tags=["[pedidos]"], dependencies=[Depends(verificar_token)])

@order_router.get("")
async def pedidos():
    return {"mensagem": "Rota de pedidos!"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: sessionmaker = Depends(pegar_sessao)):
    novo_pedido = Pedido(user=pedido_schema.user_id)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: sessionmaker = Depends(pegar_sessao), user: User = Depends(verificar_token)):
    #user.admin = True
    #user.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    if not user.admin and pedido.user != user.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar este pedido.")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido número: {pedido.id} cancelado com sucesso.",
        "pedido": pedido
        }
    

@order_router.get("/listar")
async def listar_pedidos(session: sessionmaker = Depends(pegar_sessao), user: User = Depends(verificar_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar essa operação.")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
        
@order_router.post("/pedido/adicionar_item/{id_pedido}")
async def adicionar_item_pedido(item_pedido_schema: ItemPedidoSchema, id_pedido: int, session: sessionmaker = Depends(pegar_sessao), user: User = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    if not user.admin and user.id != pedido.user:
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar itens a este pedido.")
    
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    session.add(item_pedido)
    session.commit()
    
    session.refresh(pedido)
    pedido.calcular_preco()
    session.commit()
    
    return {
        "mensagem": f"Item adicionado ao pedido",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }
    
    
@order_router.post("/pedido/remover_item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, 
                              session: sessionmaker = Depends(pegar_sessao), 
                              user: User = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item do pedido não encontrado.")
    if not user.admin and user.id != pedido.user:
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar itens a este pedido.")
    
    
    session.delete(item_pedido)
    session.commit()
    
    session.refresh(pedido)
    pedido.calcular_preco()
    session.commit()
    
    return {
        "mensagem": f"Item removido do pedido",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }
    
    
# finalizar um pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, 
                          session: sessionmaker = Depends(pegar_sessao), 
                          user: User = Depends(verificar_token)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    if not user.admin and pedido.user != user.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para finalizar este pedido.")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"Pedido número: {pedido.id} finalizado com sucesso.",
        "pedido": pedido
        }

# vizualizar 1 pedido
@order_router.get("/pedido/{id_pedido}")
async def vizualizar_pedido(id_pedido: int,
                            session: sessionmaker = Depends(pegar_sessao),
                            user: User = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    if not user.admin and pedido.user != user.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para vizualizar este pedido.")
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# vizualizar todos os pedido de 1 usuario
@order_router.get("/listar/meus-pedidos", response_model=List[ResponsePedidoSchema])
async def vizualizar_meus_pedidos(session: sessionmaker = Depends(pegar_sessao),
                                  user: User = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==user.id).all()
    return pedidos