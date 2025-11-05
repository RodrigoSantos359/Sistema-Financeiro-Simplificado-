from modules.conta.schemas import ContaCreate
from core.db import DataBase

class ContaRepository:
    QUERY_LISTAR_CONTAS = "SELECT id, nome, saldo_inicial FROM conta ORDER BY id"
    QUERY_BUSCAR_CONTA_ID = "SELECT id, nome, saldo_inicial FROM conta WHERE id = $1"
    QUERY_CRIAR_CONTA = "INSERT INTO conta (nome, saldo_inicial) VALUES ($1, $2) RETURNING id"
    QUERY_ATUALIZAR_CONTA = "UPDATE conta SET nome = $1, saldo_inicial = $2 WHERE id = $3"
    QUERY_DELETAR_CONTA = "DELETE FROM conta WHERE id = $1"

    def _row_to_conta(self, row):
        if not row:
            return None
        
        return {
            "id": row[0],
            "nome": row[1],
            "saldo_inicial": row[2]
        }
    
    def list_contas(self):
        db = DataBase()
        rows = db.execute(self.QUERY_LISTAR_CONTAS)

        return [self._row_to_conta(row) for row in rows]
    
    def get_conta(self, conta_id: int):
        db = DataBase()
        row = db.execute(self.QUERY_BUSCAR_CONTA_ID % (conta_id,), many=False)

        return self._row_to_conta(row)
    
    def create_conta(self, conta: ContaCreate):
        db = DataBase()

        query = self.QUERY_CRIAR_CONTA % (
            f"'{conta.nome}'",
            f"{conta.saldo_inicial}"
        )
        row = db.commit(query)

        return self._row_to_conta(row)
    
    def atualizar_conta(self, conta_id: int, conta: ContaCreate):
        db = DataBase()

        query = self.QUERY_ATUALIZAR_CONTA % (
            f"'{conta.nome}'",
            f"{conta.saldo_inicial}",
            conta_id
        )
        db.commit(query)

        return self.get_conta(conta_id)
    
    def delete_conta(self, conta_id: int):
        db = DataBase()
        db.commit(self.QUERY_DELETAR_CONTA % (conta_id,))

        return {"message": "Conta deletada com sucesso"}

