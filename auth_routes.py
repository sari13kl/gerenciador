from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import pegar_sessao, verificar_token
from sqlalchemy.orm import sessionmaker
from security import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone



auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def criar_token(id_usuario, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duration_token
    dic_info = {"sub":  str(id_usuario),"exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado
    # JWT
    # id_usuario
    # data_expiracao
    token = f"gsbgbdiuh8we992h{id_usuario}"
    return token


def autenticar_usuario(email, password, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user
    


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
    
#LOGIN -> EMAIL + SENHA -> TOKEN JWT
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: sessionmaker = Depends(pegar_sessao)):
    user = autenticar_usuario(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas!")
    else:
        access_token = criar_token(user.id)
        refresh_token = criar_token(user.id, duration_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }
        
@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verificar_token)):
    access_token = criar_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }