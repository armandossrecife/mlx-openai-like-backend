from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import ChatSessionCreate, ChatSessionOut, ChatMessageOut
from app.routers.deps import get_current_user

router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("", response_model=ChatSessionOut)
def create_chat(
    data: ChatSessionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    title = (data.title or "Novo Chat").strip()
    chat = ChatSession(user_id=user.id, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return ChatSessionOut(id=chat.id, title=chat.title, created_at=chat.created_at)

@router.get("", response_model=list[ChatSessionOut])
def list_chats(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = db.execute(
        select(ChatSession).where(ChatSession.user_id == user.id).order_by(ChatSession.created_at.desc())
    ).scalars().all()
    return [ChatSessionOut(id=c.id, title=c.title, created_at=c.created_at) for c in rows]

@router.get("/{chat_id}/messages", response_model=list[ChatMessageOut])
def get_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    chat = db.execute(
        select(ChatSession).where(ChatSession.id == chat_id, ChatSession.user_id == user.id)
    ).scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat não encontrado")

    msgs = db.execute(
        select(ChatMessage).where(ChatMessage.session_id == chat_id).order_by(ChatMessage.created_at.asc())
    ).scalars().all()
    return [ChatMessageOut(id=m.id, role=m.role, content=m.content, created_at=m.created_at) for m in msgs]