from fastapi import Depends
from core.db import get_db, DataBase
from modules.pagamento import schemas
from modules.pagamento.repositore import PagamentoRepository

class PagamentoService:
    def __init__(self, db: DataBase = Depends(get_db)):
        self.repository = PagamentoRepository(db)

    async def create_pagamento(self, pagamento: schemas.PagamentoCreate):
        return await self.repository.create_pagamento(pagamento)

    async def get_pagamento(self, pagamento_id: int):
        return await self.repository.get_pagamento(pagamento_id)

    async def list_pagamentos(self):
        return await self.repository.list_pagamentos()

    async def delete_pagamento(self, pagamento_id: int):
        return await self.repository.delete_pagamento(pagamento_id)

    async def update_pagamento(self, pagamento_id: int, pagamento: schemas.PagamentoCreate):
        return await self.repository.update_pagamento(pagamento_id, pagamento)