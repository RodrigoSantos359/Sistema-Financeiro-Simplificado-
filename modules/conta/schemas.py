from pydantic import BaseModel
from typing import Optional

class ContaCreate(BaseModel):
    nome: str
    saldo_inicial: float


class ContaUpdate(BaseModel):
    nome: Optional[str] = None
    saldo_inicial: Optional[float] = None


class Conta(ContaCreate):
    id: int
    ativo: bool = True

    class Config:
        orm_mode = True
