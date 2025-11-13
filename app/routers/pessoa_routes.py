from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from core.db import get_db, DataBase
from modules.pessoa.schemas import PessoaCreate, PessoaUpdate, Pessoa

router = APIRouter(prefix='/pessoas', tags=['pessoas'])

@router.get('/', response_model=List[Pessoa])
def list_pessoas(
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (cliente/fornecedor)"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    db: DataBase = Depends(get_db)
):
    query = "SELECT id, nome, tipo, ativo FROM pessoa WHERE 1=1"
    params = []
    
    if nome:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome}%")
    
    if tipo:
        if tipo not in ('cliente', 'fornecedor'):
            raise HTTPException(status_code=400, detail='tipo deve ser cliente ou fornecedor')
        query += " AND tipo = %s"
        params.append(tipo)
    
    if ativo is not None:
        query += " AND ativo = %s"
        params.append(ativo)
    
    query += " ORDER BY id"
    
    rows = db.execute(query, tuple(params) if params else None)
    return [dict(row) for row in rows]

@router.get('/{id}', response_model=Pessoa)
def get_pessoa(id: int, db: DataBase = Depends(get_db)):
    row = db.execute_one(
        "SELECT id, nome, tipo, ativo FROM pessoa WHERE id = %s",
        (id,)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Pessoa não encontrada')
    return dict(row)

@router.post('/', response_model=Pessoa, status_code=201)
def create_pessoa(payload: PessoaCreate, db: DataBase = Depends(get_db)):
    if payload.tipo not in ('cliente', 'fornecedor'):
        raise HTTPException(status_code=400, detail='tipo deve ser cliente ou fornecedor')
    
    row = db.commit(
        "INSERT INTO pessoa (nome, tipo, ativo) VALUES (%s, %s, %s) RETURNING id, nome, tipo, ativo",
        (payload.nome, payload.tipo, True)
    )
    return dict(row)

@router.put('/{id}', response_model=Pessoa)
def update_pessoa(id: int, payload: PessoaUpdate, db: DataBase = Depends(get_db)):
    # Verificar se a pessoa existe
    pessoa = db.execute_one("SELECT id FROM pessoa WHERE id = %s", (id,))
    if not pessoa:
        raise HTTPException(status_code=404, detail='Pessoa não encontrada')
    
    # Construir query de atualização dinamicamente
    updates = []
    params = []
    
    if payload.nome is not None:
        updates.append("nome = %s")
        params.append(payload.nome)
    
    if payload.tipo is not None:
        if payload.tipo not in ('cliente', 'fornecedor'):
            raise HTTPException(status_code=400, detail='tipo deve ser cliente ou fornecedor')
        updates.append("tipo = %s")
        params.append(payload.tipo)
    
    if not updates:
        # Se não há atualizações, retornar a pessoa atual
        return get_pessoa(id, db)
    
    params.append(id)
    query = f"UPDATE pessoa SET {', '.join(updates)} WHERE id = %s RETURNING id, nome, tipo, ativo"
    
    row = db.commit(query, tuple(params))
    return dict(row)

@router.patch('/{id}/desativar', status_code=204)
def desativar_pessoa(id: int, db: DataBase = Depends(get_db)):
    row = db.commit(
        "UPDATE pessoa SET ativo = %s WHERE id = %s RETURNING id",
        (False, id)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Pessoa não encontrada')
    return None
