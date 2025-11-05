from fastapi import Depends
from core.db import get_db, DataBase
from modules.conta import schemas
from modules.conta.repositore import ContaRepository

class ContaService:
    def __init__(self, db: DataBase = Depends(get_db)):
        self.repository = ContaRepository(db)

    async def create_conta(self, conta: schemas.ContaCreate):
        return await self.repository.create_conta(conta)

    async def get_conta(self, conta_id: int):
        return await self.repository.get_conta(conta_id)

    async def list_contas(self):
        return await self.repository.list_contas()

    async def delete_conta(self, conta_id: int):
        return await self.repository.delete_conta(conta_id)

    async def update_conta(self, conta_id: int, conta: schemas.ContaCreate):
        return await self.repository.update_conta(conta_id, conta)