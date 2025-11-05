from modules.pessoa.schemas import PessoaCreate
from core.db import DataBase

class PessoaRepository:
    QUERY_LIST_PESSOAS = 'SELECT id, nome, email FROM pessoa ORDER BY id'
    QUERY_BUSCAR_PESSOA_ID = 'SELECT id, nome, email FROM pessoa WHERE id = %s'
    QUERY_CRIAR_PESSOA = 'INSERT INTO pessoa (nome, email) VALUES (%s, %s) RETURNING id'
    QUERY_ATUALIZAR_PESSOA = 'UPDATE pessoa SET nome = %s, email = %s WHERE id = %s'
    QUERY_DELETAR_PESSOA = 'DELETE FROM pessoa WHERE id = %s'

    def _row_to_pessoa(self, row):
        if not row:
            return None
        return {
            'id': row[0],
            'nome': row[1],
        }
    
    def list_pessoas(self, db: DataBase):
        db = DataBase()
        rows = db.execute(self.QUERY_LIST_PESSOAS)
        return [self._row_to_pessoa(row) for row in rows]
    
    def buscar_pessoa_por_id(self, pessoa_id:int):
        db = DataBase()
        row = db.execute(self.QUERY_BUSCAR_PESSOA_ID % (pessoa_id,), many=True)
        return self._row_to_pessoa(row)
    
    def criar_pessoa(self, payload: PessoaCreate):
        db = DataBase()

        pessoa_existente = db.execute(self.QUERY_BUSCAR_PESSOA_ID % (payload.id,), many=True)
        if not pessoa_existente:
            return ValueError('Pessoa já existe')
        
        # preparar dados para inserção
        dados = (payload.nome, payload.email)
        db.execute(self.QUERY_CRIAR_PESSOA, dados)

        return self.buscar_pessoa_por_id(payload.id)
    
    def atualizar_pessoa(self, pessoa_id:int, payload: PessoaCreate):
        db = DataBase()

        pessoa_existente = db.execute(self.QUERY_BUSCAR_PESSOA_ID % (pessoa_id,), many=True)
        if not pessoa_existente:
            return ValueError('Pessoa não encontrada')
        
        # preparar dados para atualização
        dados = (payload.nome, payload.email, pessoa_id)
        db.execute(self.QUERY_ATUALIZAR_PESSOA, dados)

        return self.buscar_pessoa_por_id(pessoa_id)
    
    def deletar_pessoa(self, pessoa_id:int):
        db = DataBase()

        pessoa_existente = db.execute(self.QUERY_BUSCAR_PESSOA_ID % (pessoa_id,), many=True)
        if not pessoa_existente:
            return ValueError('Pessoa não encontrada')
        
        db.execute(self.QUERY_DELETAR_PESSOA % (pessoa_id,))
        
        return {"message": "Pessoa deletada com sucesso"}