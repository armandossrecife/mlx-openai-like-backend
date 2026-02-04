from fastapi import APIRouter, Depends, HTTPException
from app.services.mlx_client import MlxClient
from app.routers.deps import get_mlx_client
from app.routers.deps import get_current_user, get_mlx_client
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.models import ModelListResponse, ModelInfo

router = APIRouter(tags=["models"])

@router.get("/models", response_model=ModelListResponse)
async def list_models(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    client: MlxClient = Depends(get_mlx_client)
):
    """
    Lista todos os modelos LLM disponíveis no servidor OpenAI Like (Ollama).
    
    Retorna:
        ModelListResponse: Lista de modelos com informações básicas
    """
    try:
        # Chama o endpoint /v1/models do servidor LLM
        models_response = await client.list_models()
        
        if not models_response or "data" not in models_response:
            raise HTTPException(
                status_code=502, 
                detail="Resposta inválida do servidor LLM"
            )
        
        # Formata a resposta no padrão OpenAI
        return ModelListResponse(
            object="list",
            data=[
                ModelInfo(
                    id=model["id"],
                    object=model["object"],
                    created=model["created"],
                    owned_by=model["owned_by"]
                )
                for model in models_response["data"]
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao buscar modelos: {str(e)}"
        )