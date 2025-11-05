from fastapi import Depends
from core.db import get_db, DataBase
from modules.pessoa import schemas
from modules.pessoa.repositore import PessoaRepository

class PessoaService:
    def __init__(self, db: DataBase = Depends(get_db)):
        self.repository = PessoaRepository(db)

    async def create_pessoa(self, pessoa: schemas.PessoaCreate):
        return await self.repository.create_pessoa(pessoa)

    async def get_pessoa(self, pessoa_id: int):
        return await self.repository.get_pessoa(pessoa_id)

    async def list_pessoas(self):
        return await self.repository.list_pessoas()

    async def delete_pessoa(self, pessoa_id: int):
        return await self.repository.delete_pessoa(pessoa_id)

    async def update_pessoa(self, pessoa_id: int, pessoa: schemas.PessoaCreate):
        return await self.repository.update_pessoa(pessoa_id, pessoa)