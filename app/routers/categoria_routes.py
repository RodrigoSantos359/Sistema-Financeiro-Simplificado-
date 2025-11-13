from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from core.db import get_db, DataBase
from modules.categoria.schemas import CategoriaCreate, CategoriaUpdate, Categoria

router = APIRouter(prefix='/categorias', tags=['categorias'])

@router.get('/', response_model=List[Categoria])
def list_categorias(
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (receita/despesa)"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    db: DataBase = Depends(get_db)
):
    query = "SELECT id, nome, tipo, ativo FROM categoria WHERE 1=1"
    params = []
    
    if nome:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome}%")
    
    if tipo:
        if tipo not in ('receita', 'despesa'):
            raise HTTPException(status_code=400, detail='tipo deve ser receita ou despesa')
        query += " AND tipo = %s"
        params.append(tipo)
    
    if ativo is not None:
        query += " AND ativo = %s"
        params.append(ativo)
    
    query += " ORDER BY id"
    
    rows = db.execute(query, tuple(params) if params else None)
    return [dict(row) for row in rows]

@router.get('/{id}', response_model=Categoria)
def get_categoria(id: int, db: DataBase = Depends(get_db)):
    row = db.execute_one(
        "SELECT id, nome, tipo, ativo FROM categoria WHERE id = %s",
        (id,)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return dict(row)

@router.post('/', response_model=Categoria, status_code=201)
def create_categoria(payload: CategoriaCreate, db: DataBase = Depends(get_db)):
    if payload.tipo not in ('receita', 'despesa'):
        raise HTTPException(status_code=400, detail='tipo deve ser receita ou despesa')
    
    row = db.commit(
        "INSERT INTO categoria (nome, tipo, ativo) VALUES (%s, %s, %s) RETURNING id, nome, tipo, ativo",
        (payload.nome, payload.tipo, True)
    )
    return dict(row)

@router.put('/{id}', response_model=Categoria)
def update_categoria(id: int, payload: CategoriaUpdate, db: DataBase = Depends(get_db)):
    # Verificar se a categoria existe
    categoria = db.execute_one("SELECT id FROM categoria WHERE id = %s", (id,))
    if not categoria:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    
    # Construir query de atualização dinamicamente
    updates = []
    params = []
    
    if payload.nome is not None:
        updates.append("nome = %s")
        params.append(payload.nome)
    
    if payload.tipo is not None:
        if payload.tipo not in ('receita', 'despesa'):
            raise HTTPException(status_code=400, detail='tipo deve ser receita ou despesa')
        updates.append("tipo = %s")
        params.append(payload.tipo)
    
    if not updates:
        # Se não há atualizações, retornar a categoria atual
        return get_categoria(id, db)
    
    params.append(id)
    query = f"UPDATE categoria SET {', '.join(updates)} WHERE id = %s RETURNING id, nome, tipo, ativo"
    
    row = db.commit(query, tuple(params))
    return dict(row)

@router.patch('/{id}/desativar', status_code=204)
def desativar_categoria(id: int, db: DataBase = Depends(get_db)):
    row = db.commit(
        "UPDATE categoria SET ativo = %s WHERE id = %s RETURNING id",
        (False, id)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return None
