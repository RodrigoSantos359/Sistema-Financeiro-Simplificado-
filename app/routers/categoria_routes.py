<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from core.db import get_db, DataBase
from modules.categoria.schemas import CategoriaCreate, CategoriaUpdate, Categoria
=======
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from core.db import get_db
from modules.categoria.schemas import CategoriaCreate, Categoria
>>>>>>> 8df36cda30eeeaec837af4a9e0f7d54ef24e57c6

router = APIRouter(prefix='/categorias', tags=['categorias'])

@router.get('/', response_model=List[Categoria])
<<<<<<< HEAD
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
=======
def list_categorias(db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute('SELECT id, nome, tipo FROM categoria ORDER BY id')
        rows = cur.fetchall()
    return rows

@router.get('/{id}', response_model=Categoria)
def get_categoria(id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute('SELECT id, nome, tipo FROM categoria WHERE id = %s', (id,))
        row = cur.fetchone()
>>>>>>> 8df36cda30eeeaec837af4a9e0f7d54ef24e57c6
    if not row:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return dict(row)

<<<<<<< HEAD
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
=======
@router.post('/', response_model=Categoria)
def create_categoria(payload: CategoriaCreate, db=Depends(get_db)):
    if payload.tipo not in ('receita', 'despesa'):
        raise HTTPException(status_code=400, detail='tipo deve ser receita ou despesa')
    with db.cursor() as cur:
        cur.execute(
            'INSERT INTO categoria (nome, tipo) VALUES (%s, %s) RETURNING id, nome, tipo',
            (payload.nome, payload.tipo)
        )
        row = cur.fetchone()
        db.commit()
    return row

@router.put('/{id}', response_model=Categoria)
def update_categoria(id: int, payload: CategoriaCreate, db=Depends(get_db)):
    if payload.tipo not in ('receita', 'despesa'):
        raise HTTPException(status_code=400, detail='tipo deve ser receita ou despesa')
    with db.cursor() as cur:
        cur.execute(
            'UPDATE categoria SET nome = %s, tipo = %s WHERE id = %s RETURNING id, nome, tipo',
            (payload.nome, payload.tipo, id)
        )
        row = cur.fetchone()
        db.commit()
    if not row:
>>>>>>> 8df36cda30eeeaec837af4a9e0f7d54ef24e57c6
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

<<<<<<< HEAD
@router.patch('/{id}/desativar', status_code=204)
def desativar_categoria(id: int, db: DataBase = Depends(get_db)):
    row = db.commit(
        "UPDATE categoria SET ativo = %s WHERE id = %s RETURNING id",
        (False, id)
    )
=======
@router.delete('/{id}')
def delete_categoria(id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute('DELETE FROM categoria WHERE id = %s RETURNING id', (id,))
        row = cur.fetchone()
        db.commit()
>>>>>>> 8df36cda30eeeaec837af4a9e0f7d54ef24e57c6
    if not row:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    return None
