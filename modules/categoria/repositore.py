from modules.categoria.schemas import CategoriaCreate
from core.db import DataBase

class CategoriaRepository:
    QUERY_LIST_CATEGORIAS = 'SELECT id, nome, tipo FROM categoria ORDER BY id'
    QUERY_BUSCAR_CATEGORIA_ID = 'SELECT id, nome, tipo FROM categoria WHERE id = %s'
    QUERY_CRIAR_CATEGORIA = 'INSERT INTO categoria (nome, tipo) VALUES (%s, %s) RETURNING id'
    QUERY_ATUALIZAR_CATEGORIA = 'UPDATE categoria SET nome = %s, tipo = %s WHERE id = %s'
    QUERY_DELETAR_CATEGORIA = 'DELETE FROM categoria WHERE id = %s'

    def _row_to_categoria(self, row):
        if not row:
            return None
        return {
            'id': row[0],
            'nome': row[1],
            'tipo': row[2]
        }
    
    def list_categorias(self, db: DataBase):
        db = DataBase()
        rows = db.execute(self.QUERY_LIST_CATEGORIAS)
        return [self._row_to_categoria(row) for row in rows]
    
    def buscar_categoria_por_id(self, categoria_id:int):
        db = DataBase()
        row = db.execute(self.QUERY_BUSCAR_CATEGORIA_ID % (categoria_id,), many=True)
        return self._row_to_categoria(row)
    
    def criar_categoria(self, payload: CategoriaCreate):
        db = DataBase()

        categoria_existente = db.execute(self.QUERY_BUSCAR_CATEGORIA_ID % (payload.id,), many=True)
        if not categoria_existente:
            return ValueError('Categoria já existe')
        
        # preparar dados para inserção
        dados = (payload.nome, payload.tipo)
        db.execute(self.QUERY_CRIAR_CATEGORIA, dados)

        return self.buscar_categoria_por_id(payload.id)
    
    def atualizar_categoria(self, categoria_id:int, payload: CategoriaCreate):
        db = DataBase()

        categoria_existente = db.execute(self.QUERY_BUSCAR_CATEGORIA_ID % (categoria_id,), many=True)
        if not categoria_existente:
            return ValueError('Categoria não encontrada')
        
        # preparar dados para atualização
        dados = (payload.nome, payload.tipo, categoria_id)
        db.execute(self.QUERY_ATUALIZAR_CATEGORIA, dados)

        return self.buscar_categoria_por_id(categoria_id)
    
    def deletar_categoria(self, categoria_id:int):
        db = DataBase()

        categoria_existente = db.execute(self.QUERY_BUSCAR_CATEGORIA_ID % (categoria_id,), many=True)
        if not categoria_existente:
            return ValueError('Categoria não encontrada')
        
        db.execute(self.QUERY_DELETAR_CATEGORIA % (categoria_id,))

        return {"message": "Categoria deletada com sucesso"}
    