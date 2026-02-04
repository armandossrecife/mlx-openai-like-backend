from fastapi import APIRouter, Depends
from app.schemas.mlx import HealthResponse
from app.services.mlx_client import MlxClient
from app.routers.deps import get_mlx_client

router = APIRouter(tags=["health"])

@router.get("/prompt", response_model=HealthResponse)
async def prompt_health_check(client: MlxClient = Depends(get_mlx_client)):
    try:
        resposta = await client.generate_response("O que é um teste de conexão para uma API Rest?")
        if not resposta:
            raise Exception("Client not initialized")
        print("Conexão com o MLX bem-sucedida.")
        print("Resposta de teste do MLX:", resposta)
        return HealthResponse(status="healthy", mlx_status="connected", available_models=[])

    except Exception as e:
        return HealthResponse(status="unhealthy", mlx_status=f"error: {e}", available_models=[])
    
@router.get("/health", response_model=HealthResponse)
async def health_check(client: MlxClient = Depends(get_mlx_client)):
    """
    Verificação rápida de saúde do servidor LLM.
    Usa endpoint leve (/v1/models) em vez de inferência completa.
    """
    try:
        # Checagem rápida usando endpoint de listagem de modelos
        models = await client.list_models()
        
        if models and "data" in models:
            return HealthResponse(
                status="healthy", 
                mlx_status="connected", 
                available_models=[m["id"] for m in models["data"]]
            )
        else:
            return HealthResponse(
                status="unhealthy", 
                mlx_status="error: resposta inválida", 
                available_models=[]
            )

    except Exception as e:
        return HealthResponse(
            status="unhealthy", 
            mlx_status=f"error: {str(e)}", 
            available_models=[]
        )