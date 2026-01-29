import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db, SessionLocal
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.services.mlx_client import MlxClient
from app.schemas.mlx import GenerateWithChat
from app.routers.deps import get_current_user, get_mlx_client
from app.core.config import settings    

router = APIRouter(tags=["inference"])

@router.post("/generate")
async def generate_with_auth(
    req: GenerateWithChat, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user), 
    client: MlxClient = Depends(get_mlx_client)
):
    # 1. Validação da Sessão
    chat = db.execute(
        select(ChatSession).where(ChatSession.id == req.chat_id, ChatSession.user_id == user.id)
    ).scalar_one_or_none()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Sessão de Chat não encontrada.")
    
    # 2. Salva mensagem do Usuário imediatamente
    user_msg = ChatMessage(session_id=req.chat_id, role="user", content=req.prompt)
    db.add(user_msg)
    db.commit()

    # 3. Prepara Cliente
    client = MlxClient(base_url=settings.LLM_SERVER_BASE_URL)
    
    # --- LOGICA PARA STREAMING ---
    if req.stream:
        async def response_generator():
            full_response_accumulated = ""
            try:
                # Chama o client com stream=True
                stream_obj = await client.generate_response(req.prompt, stream=True)
                
                # ... (dentro da função response_generator)
                async for chunk in stream_obj:
                    content = chunk.choices[0].delta.content or ""
                    if content:
                        full_response_accumulated += content
                        
                        # CORREÇÃO: Formato SSE estrito (data: json \n\n)
                        json_data = json.dumps({"type": "token", "chunk": content})
                        yield f"data: {json_data}\n\n"
                
                # Envia sinal de done também no formato correto
                yield f"data: {json.dumps({'type': 'done'})}\n\n"

            except Exception as e:
                yield json.dumps({"type": "error", "error": str(e)}) + "\n"
            
            finally:
                # 4. Salva a resposta completa do assistente no banco APÓS o stream terminar
                if full_response_accumulated:
                    db_stream = SessionLocal()
                    try:
                        asst_msg = ChatMessage(
                            session_id=req.chat_id, 
                            role="assistant", 
                            content=full_response_accumulated
                        )
                        db_stream.add(asst_msg)
                        db_stream.commit()
                    except Exception as e:
                        print(f"Erro ao salvar chat no banco: {e}")
                    finally:
                        db_stream.close()

        # Retorna o StreamingResponse para o Frontend Flask
        return StreamingResponse(response_generator(), media_type="application/x-ndjson")

    # --- LOGICA PADRÃO (SEM STREAM) ---
    try: 
        resposta = await client.generate_response(req.prompt, stream=False)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))        

    # Salva resposta no banco
    db.add(ChatMessage(session_id=req.chat_id, role="assistant", content=resposta))
    db.commit()

    return GenerateWithChat(
        model=req.model,
        prompt=req.prompt,
        resposta=resposta,
        chat_id=req.chat_id,
        stream=False,
        options=req.options
    )