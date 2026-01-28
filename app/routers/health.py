from fastapi import APIRouter, Depends
from app.schemas.mlx import HealthResponse
from app.services.mlx_client import MlxClient
from app.routers.deps import get_mlx_client

router = APIRouter(tags=["health"])

@router.get("/health", response_model=HealthResponse)
async def health_check(client: MlxClient = Depends(get_mlx_client)):
    try:
        resposta = await client.generate_response("O que é um teste de conexão para uma API Rest?")
        if not resposta:
            raise Exception("Client not initialized")
        print("Conexão com o MLX bem-sucedida.")
        print("Resposta de teste do MLX:", resposta)
        return HealthResponse(status="healthy", mlx_status="connected", available_models=[])

    except Exception as e:
        return HealthResponse(status="unhealthy", mlx_status=f"error: {e}", available_models=[])