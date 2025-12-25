from fastapi import APIRouter, Depends
from models import User
from dependencies import pegar_sessao
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("")
async def home():
    """"
    Rota padrão de pedidos . Todas precisam ser autenticadas
    """
    return {"mensagem": "Rota de autenticação!", "autenticado": False}

@auth_router.post("/cadastre")
async def register_user(email: str, password: str, name: str, session: sessionmaker = Depends(pegar_sessao)):
    user = session.query(User).filter(User.email==email).first()
    if user:
        #já existe um usuário com esse email
        return {"mensagem": "Já existe um usuário cadastrado com esse email!"}
    else:
        password_cript = bcrypt_context.hash(password)
        new_user = User(name, email, password_cript)
        session.add(new_user)
        session.commit()
        return {"mensagem": "Usuário cadastrado com sucesso!"}
    