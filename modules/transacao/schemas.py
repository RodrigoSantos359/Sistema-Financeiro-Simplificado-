from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class TransacaoCreate(BaseModel):
    conta_id: int
    categoria_id: int
    valor: float
    data: datetime
    descricao: Optional[str] = None


class TransacaoUpdate(BaseModel):
    conta_id: Optional[int] = None
    categoria_id: Optional[int] = None
    valor: Optional[float] = None
    data: Optional[datetime] = None
    descricao: Optional[str] = None


class Transacao(TransacaoCreate):
    id: int
    ativo: bool = True
    
    class Config:
        orm_mode = True