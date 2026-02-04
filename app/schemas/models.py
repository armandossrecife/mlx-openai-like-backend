from typing import List
from pydantic import BaseModel

# Schema para resposta de modelos
class ModelInfo(BaseModel):
    id: str
    object: str
    created: int
    owned_by: str

class ModelListResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]