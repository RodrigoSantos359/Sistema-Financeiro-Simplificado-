from modules.transacao.schemas import TransacaoCreate
from core.db import DataBase

class TransacaoRepository:
    QUERY_LIST_TRANSACOES = 'SELECT id, valor, data, tipo, pessoa_id FROM transacao ORDER BY id'
    QUERY_BUSCAR_TRANSACAO_ID = 'SELECT id, valor, data, tipo, descricao, pessoa_id FROM transacao WHERE id = %s'
    QUERY_CRIAR_TRANSACAO = 'INSERT INTO transacao (valor, data, tipo, descricao, pessoa_id) VALUES (%s, %s, %s, %s, %s) RETURNING id'
    QUERY_ATUALIZAR_TRANSACAO = 'UPDATE transacao SET valor = %s, data = %s, tipo = %s, descricao = %s, pessoa_id = %s WHERE id = %s'
    QUERY_DELETAR_TRANSACAO = 'DELETE FROM transacao WHERE id = %s'

    def _row_to_transacao(self, row):
        if not row:
            return None
        return {
            'id': row[0],
            'valor': row[1],
            'data': row[2],
            'tipo': row[3],
            'descricao': row[4],
            'pessoa_id': row[5],
            'categoria_id': row[6]
        }
    
    def list_transacoes(self, db: DataBase):
        db = DataBase()
        rows = db.execute(self.QUERY_LIST_TRANSACOES)

        return [self._row_to_transacao(row) for row in rows]
    
    def buscar_transacao_por_id(self, transacao_id:int):
        db = DataBase()
        row = db.execute(self.QUERY_BUSCAR_TRANSACAO_ID % (transacao_id,), many=True)

        return self._row_to_transacao(row)
    
    def criar_transacao(self, payload: TransacaoCreate):
        db = DataBase()
        db.execute(self.QUERY_CRIAR_TRANSACAO, (payload.valor, payload.data, payload.tipo, payload.pessoa_id))

        return self.buscar_transacao_por_id(payload.id)
    
    def atualizar_transacao(self, transacao_id:int, payload: TransacaoCreate):
        db = DataBase()

        transacao_existente = db.execute(self.QUERY_BUSCAR_TRANSACAO_ID % (transacao_id,), many=True)
        if not transacao_existente:
            return ValueError('Transação não encontrada')
        # preparar dados para atualização
        dados = (payload.valor, payload.data, payload.tipo, payload.pessoa_id, transacao_id)
        db.execute(self.QUERY_ATUALIZAR_TRANSACAO, dados)

        return self.buscar_transacao_por_id(transacao_id)
    
    def deletar_transacao(self, transacao_id:int):
        db = DataBase()
        transacao_existente = db.execute(self.QUERY_BUSCAR_TRANSACAO_ID % (transacao_id,), many=True)
        if not transacao_existente:
            return ValueError('Transação não encontrada')
        db.execute(self.QUERY_DELETAR_TRANSACAO, (transacao_id,))

        return {"message": "Transação deletada com sucesso"}