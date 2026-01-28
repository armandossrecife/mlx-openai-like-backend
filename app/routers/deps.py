from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

from app.services.mlx_client import MlxClient

bearer = HTTPBearer(auto_error=False)

_mlx_client_instance = None

def get_mlx_client() -> MlxClient:
    global _mlx_client_instance
    if _mlx_client_instance is None:
        # Pega a URL do settings (ex: settings.MLX_URL)
        _mlx_client_instance = MlxClient() 
    return _mlx_client_instance

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    if not creds:
        raise HTTPException(status_code=401, detail="Token ausente")

    try:
        payload = decode_token(creds.credentials)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user