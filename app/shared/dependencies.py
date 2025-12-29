from core.models import db, User
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from core.security import SECRET_KEY, ALGORITHM, oauth2_scheme


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
        

def verificar_token(token: str = Depends(oauth2_scheme), session: sessionmaker = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = dic_info.get("sub")
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
    #verificar se o token é válido
    #extrair o id do usuário do token
    user = session.query(User).filter(User.id==id_usuario).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso inválido! Usuário não encontrado.")
    return user