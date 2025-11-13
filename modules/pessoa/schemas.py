from pydantic import BaseModel
from typing import Literal, Optional


TipoPessoaEnum = Literal['cliente', 'fornecedor']

class PessoaCreate(BaseModel):
    nome: str
    tipo: TipoPessoaEnum   


class PessoaUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[TipoPessoaEnum] = None


class Pessoa(PessoaCreate):
    id: int
    ativo: bool = True

    class Config:
        orm_mode = True
