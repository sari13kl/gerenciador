from fastapi.security import OAuth2PasswordBearer
import os
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# usar bcrypt_sha256 como esquema preferencial (pré-hash com SHA256 antes de aplicar bcrypt)
# isso evita o erro de limite de 72 bytes do bcrypt e mantém 'bcrypt' como fallback
bcrypt_context = CryptContext(schemes=["argon2","bcrypt_sha256", "bcrypt"], deprecated="auto")
