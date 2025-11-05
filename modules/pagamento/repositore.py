from modules.pagamento.schemas import PagamentoCreate
from core.db import DataBase

class PagamentoRepository:
    QUERY_LIST_PAGAMENTOS = 'SELECT id, valor, data, categoria_id FROM pagamento ORDER BY id'
    QUERY_BUSCAR_PAGAMENTO_ID = 'SELECT id, valor, data, categoria_id FROM pagamento WHERE id = %s'
    QUERY_CRIAR_PAGAMENTO = 'INSERT INTO pagamento (valor, data, categoria_id) VALUES (%s, %s, %s) RETURNING id'
    QUERY_ATUALIZAR_PAGAMENTO = 'UPDATE pagamento SET valor = %s, data = %s, categoria_id = %s WHERE id = %s'
    QUERY_DELETAR_PAGAMENTO = 'DELETE FROM pagamento WHERE id = %s'

    def _row_to_pagamento(self, row):
        if not row:
            return None
        return {
            'id': row[0],
            'transacao': row[1],
            'status': row[2],
            'data_pagamento': row[3],
            'categoria_id': row[4]
        }
    
    def list_pagamentos(self, db: DataBase):
        db = DataBase()
        rows = db.execute(self.QUERY_LIST_PAGAMENTOS)
        return [self._row_to_pagamento(row) for row in rows]
    
    def buscar_pagamento_por_id(self, pagamento_id:int):
        db = DataBase()
        row = db.execute(self.QUERY_BUSCAR_PAGAMENTO_ID % (pagamento_id,), many=True)
        return self._row_to_pagamento(row)
    
    def criar_pagamento(self, payload: PagamentoCreate):
        db = DataBase()

        pagamento_existente = db.execute(self.QUERY_BUSCAR_PAGAMENTO_ID % (payload.id,), many=True)
        if not pagamento_existente:
            return ValueError('Pagamento já existe')
        
        # preparar dados para inserção
        dados = (payload.valor, payload.data, payload.categoria_id)
        db.execute(self.QUERY_CRIAR_PAGAMENTO, dados)

        return self.buscar_pagamento_por_id(payload.id)
    
    def atualizar_pagamento(self, pagamento_id:int, payload: PagamentoCreate):
        db = DataBase()

        pagamento_existente = db.execute(self.QUERY_BUSCAR_PAGAMENTO_ID % (pagamento_id,), many=True)
        if not pagamento_existente:
            return ValueError('Pagamento não encontrado')
        
        # preparar dados para atualização
        dados = (payload.valor, payload.data, payload.categoria_id, pagamento_id)
        db.execute(self.QUERY_ATUALIZAR_PAGAMENTO, dados)

        return self.buscar_pagamento_por_id(pagamento_id)
    
    def deletar_pagamento(self, pagamento_id:int):
        db = DataBase()

        pagamento_existente = db.execute(self.QUERY_BUSCAR_PAGAMENTO_ID % (pagamento_id,), many=True)
        if not pagamento_existente:
            return ValueError('Pagamento não encontrado')
        
        db.execute(self.QUERY_DELETAR_PAGAMENTO % (pagamento_id,))

        return {"message": "Pagamento deletado com sucesso"}
    