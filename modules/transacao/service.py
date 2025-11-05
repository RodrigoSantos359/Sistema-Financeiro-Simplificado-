from fastapi import Depends
from core.db import get_db, DataBase
from modules.transacao import schemas
from modules.transacao.repositore import TransacaoRepository

class TransacaoService:
    def __init__(self, db: DataBase = Depends(get_db)):
        self.repository = TransacaoRepository(db)
    async def create_transacao(self, transacao: schemas.TransacaoCreate):
        return await self.repository.create_transacao(transacao)
    
    async def get_transacao(self, transacao_id: int):
        return await self.repository.get_transacao(transacao_id)
    
    async def list_transacoes(self):
        return await self.repository.list_transacoes()
    
    async def delete_transacao(self, transacao_id: int):
        return await self.repository.delete_transacao(transacao_id)
    
    async def update_transacao(self, transacao_id: int, transacao: schemas.TransacaoCreate):
        return await self.repository.update_transacao(transacao_id, transacao)
    