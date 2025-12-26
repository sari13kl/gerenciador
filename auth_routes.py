from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import pegar_sessao
from sqlalchemy.orm import sessionmaker
from main import bcrypt_context
from schemas import UserSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("")
async def home():
    """"
    Rota padrão de pedidos . Todas precisam ser autenticadas
    """
    return {"mensagem": "Rota de autenticação!", "autenticado": False}

@auth_router.post("/cadastre")
async def register_user(user_schema: UserSchema, session: sessionmaker = Depends(pegar_sessao)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        #já existe um usuário com esse email
        raise HTTPException(status_code=400, detail="Já existe um usuário cadastrado com esse email!")
    else:
        password_script = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, password_script, user_schema.ativo, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"mensagem": f"Usuário {user_schema.name} cadastrado com sucesso!"}