from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class GenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False
    options: Optional[Dict[str, Any]] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None

class GenerateWithChat(BaseModel):
    model: str
    prompt: str
    resposta: Optional[str] = None
    chat_id: int
    stream: bool = False
    options: Optional[Dict[str, Any]] = None
    
class HealthResponse(BaseModel):
    status: str
    mlx_status: str
    available_models: List[str] = []