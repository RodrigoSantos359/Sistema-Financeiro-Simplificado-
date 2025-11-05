from fastapi import Depends
from core.db import get_db, DataBase
from modules.categoria import schemas
from modules.categoria.repositore import CategoriaRepository

class CategoriaService:
    def __init__(self, db: DataBase = Depends(get_db)):
        self.repository = CategoriaRepository(db)

    async def create_categoria(self, categoria: schemas.CategoriaCreate):
        return await self.repository.create_categoria(categoria)

    async def get_categoria(self, categoria_id: int):
        return await self.repository.get_categoria(categoria_id)

    async def list_categorias(self):
        return await self.repository.list_categorias()

    async def delete_categoria(self, categoria_id: int):
        return await self.repository.delete_categoria(categoria_id)

    async def update_categoria(self, categoria_id: int, categoria: schemas.CategoriaCreate):
        return await self.repository.update_categoria(categoria_id, categoria)