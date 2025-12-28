from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


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

    # STATUS_PEDIDO = (
    # ("PENDENTE", "PENDENTE"),
    # ("FINALIZADO", "FINALIZADO"),
    # ("CANCELADO", "CANCELADO"),
    # )
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("users.id")) # chave estrangeira users.id
    preco = Column("preco", Float)
    #itens =

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status
        
    def calcular_preco(self):
        pass

#ItensPedido
class ItemPedido(Base):
    __tablename__ = "pedido_itens"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))
    
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

#execução
