from fastapi import APIRouter, Depends, HTTPException
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
async def generate_with_auth(req: GenerateWithChat, db: Session = Depends(get_db),user: User = Depends(get_current_user), client: MlxClient = Depends(get_mlx_client)):
    # Verifica se a sessão de chat pertence ao usuário autenticado
    chat = db.execute(
        select(ChatSession).where(ChatSession.id == req.chat_id, ChatSession.user_id == user.id)
    ).scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Sessão de Chat não encontrada para o usuário autenticado.")
    
    # Adiciona a mensagem do usuário ao banco de dados
    user_msg = ChatMessage(session_id=req.chat_id, role="user", content=req.prompt)
    db.add(user_msg)
    db.commit()

    # Envia a solicitação ao MLX Server e obtém a resposta
    client = MlxClient(base_url=settings.LLM_SERVER_BASE_URL)
    payload = {"model": req.model, "prompt": req.prompt, "stream": False}
    if req.options:
        payload["options"] = req.options
        
    try: 
        # A mágica acontece aqui: await não trava o servidor
        resposta = await client.generate_response(req.prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))        

    # Adiciona a resposta do assistente ao banco de dados
    db2 = SessionLocal()
    try:
        db2.add(ChatMessage(session_id=req.chat_id, role="assistant", content=resposta))
        db2.commit()
    finally:
        db2.close()

    return GenerateWithChat(
        model=req.model,
        prompt=req.prompt,
        resposta=resposta,
        chat_id=req.chat_id,
        stream=False,
        options=req.options
    )