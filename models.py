from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import ChoiceType


#conexão com o banco
db = create_engine("sqlite:///bank.db")

#base do banco
Base = declarative_base()

#classes/tabelas
class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, ativo=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.ativo = ativo
        self.admin = admin

#Pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # PENDENTE, FINALIZADO, CANCELADO
    usuario = Column("usuario", ForeignKey("users.id")) # chave estrangeira users.id
    preco = Column("preco", Float)
    #itens =

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status


#ItensPedido


#execução