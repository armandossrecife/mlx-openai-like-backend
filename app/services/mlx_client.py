import logging
from typing import Optional
from openai import AsyncOpenAI, APIConnectionError, APIStatusError
from app.core.config import settings

# Configuração de Logs (Muito melhor que print)
logger = logging.getLogger(__name__)

class MlxClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        # Prioriza o argumento passado, senão pega do settings, senão usa default
        final_url = base_url or settings.LLM_SERVER_BASE_URL or "http://localhost:8080/v1"
        
        self.client = AsyncOpenAI(
            base_url=final_url,
            api_key=api_key or "nao-necessaria-localmente"
        )

    async def generate_response(self, pergunta: str) -> str:        
        """
        Gera uma resposta do modelo MLX de forma assíncrona.
        Lança exceções para serem tratadas pela rota/controller.
        """
        try:
            logger.info(f"Enviando prompt para MLX: {pergunta[:10]}...")
            
            # Note o 'await' aqui. Isso libera o servidor para atender outros usuários
            response = await self.client.chat.completions.create(
                model=settings.MODELO_LLM,
                messages=[
                    {"role": "system", "content": "Você é um assistente útil e conciso."},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.7,
                stream=False
            )
            
            content = response.choices[0].message.content
            logger.info("Resposta recebida com sucesso.")
            return content

        except APIConnectionError as e:
            logger.error(f"Não foi possível conectar ao servidor MLX: {e}")
            # Re-lançamos o erro ou criamos um customizado para o FastAPI pegar
            raise Exception("Servidor de IA indisponível") from e
            
        except APIStatusError as e:
            logger.error(f"Erro de status da API MLX ({e.status_code}): {e.message}")
            raise Exception(f"Erro no processamento da IA: {e.message}") from e

        except Exception as e:
            logger.error(f"Erro inesperado no cliente MLX: {e}")
            raise Exception("Erro inesperado ao comunicar com o servidor de IA") from e