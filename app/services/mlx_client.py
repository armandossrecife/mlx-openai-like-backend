# instrucao 2 - MlxClient atualizado para suportar streaming

import logging
from typing import Optional, Union, AsyncGenerator, Dict, Any
from openai import AsyncOpenAI, APIConnectionError, APIStatusError
from openai.types.chat import ChatCompletionChunk
from app.core.config import settings
import httpx

logger = logging.getLogger(__name__)

class MlxClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        final_url = base_url or settings.LLM_SERVER_BASE_URL or "http://localhost:8080/v1"
        
        self.final_url = final_url
        
        self.client = AsyncOpenAI(
            base_url=final_url,
            api_key=api_key or "nao-necessaria-localmente"
        )
        
        self.timeout = 30  # Timeout padrão para requisições

    # Agora retorna str (se stream=False) ou AsyncGenerator (se stream=True)
    async def generate_response(self, pergunta: str, stream: bool = False) -> Union[str, AsyncGenerator[ChatCompletionChunk, None]]:        
        """
        Gera uma resposta do modelo MLX.
        Se stream=True, retorna um gerador assíncrono.
        Se stream=False, retorna a string completa.
        """
        try:
            logger.info(f"Enviando prompt para MLX (Stream={stream}): {pergunta[:10]}...")
            
            response = await self.client.chat.completions.create(
                model=settings.MODELO_LLM,
                messages=[
                    {"role": "system", "content": "Você é um assistente útil e conciso."},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.7,
                stream=stream # Passamos o parâmetro dinamicamente
            )
            
            if stream:
                # Retorna o objeto de stream para ser iterado pelo chamador
                return response
            else:
                # Comportamento antigo: pega o texto completo
                content = response.choices[0].message.content
                logger.info("Resposta completa recebida com sucesso.")
                return content

        except APIConnectionError as e:
            logger.error(f"Não foi possível conectar ao servidor MLX: {e}")
            raise Exception("Servidor de IA indisponível") from e
            
        except APIStatusError as e:
            logger.error(f"Erro de status da API MLX ({e.status_code}): {e.message}")
            raise Exception(f"Erro no processamento da IA: {e.message}") from e

        except Exception as e:
            logger.error(f"Erro inesperado no cliente MLX: {e}")
            raise Exception("Erro inesperado ao comunicar com o servidor de IA") from e
        
        
    async def list_models(self) -> Dict[str, Any]:
        """
        Lista os modelos disponíveis no servidor OpenAI Like.
        
        Retorna:
            Dict[str, Any]: Resposta JSON com lista de modelos
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.final_url}/models")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise Exception(f"Erro na requisição HTTP: {str(e)}")