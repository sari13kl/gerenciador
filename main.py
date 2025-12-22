from fastapi import FastAPI
import uvicorn

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

#para rodar o servidor, use o comando:
# uvicorn main:app --reload
#endpoint:
#/ordens(caminho)

# Rest APIs
# Get -> leitura/pegar
# Post -> enviar/criar
# Put/Patch -> atualizar/editar
# Delete -> deletar/remover