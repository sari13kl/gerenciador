from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from modules.auth_routes import auth_router
from modules.order_routes import order_router



app = FastAPI()


app.include_router(auth_router)
app.include_router(order_router)


#para rodar o servidor, use o comando:
# uvicorn main:app --reload
#endpoint:
#/ordens(caminho)

# Rest APIs
# Get -> leitura/pegar
# Post -> enviar/criar
# Put/Patch -> atualizar/editar
# Delete -> deletar/remover