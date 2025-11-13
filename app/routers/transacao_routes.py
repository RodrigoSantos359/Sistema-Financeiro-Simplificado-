<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from core.db import get_db, DataBase
from modules.transacao.schemas import TransacaoCreate, TransacaoUpdate, Transacao
=======
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from core.db import get_db
from modules.transacao.schemas import TransacaoCreate, Transacao
>>>>>>> 8df36cda30eeeaec837af4a9e0f7d54ef24e57c6

router = APIRouter(prefix="/transacoes", tags=["transacoes"])

<<<<<<< HEAD
@router.get('/', response_model=List[Transacao])
def list_transacoes(
    conta_id: Optional[int] = Query(None, description="Filtrar por conta"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoria"),
    data_ini: Optional[datetime] = Query(None, description="Data inicial (ISO 8601)"),
    data_fim: Optional[datetime] = Query(None, description="Data final (ISO 8601)"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    db: DataBase = Depends(get_db)
):
    query = "SELECT id, conta_id, categoria_id, valor, data, descricao, ativo FROM transacao WHERE 1=1"
    params = []
    
    if conta_id:
        query += " AND conta_id = %s"
        params.append(conta_id)
    
    if categoria_id:
        query += " AND categoria_id = %s"
        params.append(categoria_id)
    
    if data_ini:
        query += " AND data >= %s"
        params.append(data_ini)
    
    if data_fim:
        query += " AND data <= %s"
        params.append(data_fim)
    
    if ativo is not None:
        query += " AND ativo = %s"
        params.append(ativo)
    
    query += " ORDER BY id"
    
    rows = db.execute(query, tuple(params) if params else None)
    return [dict(row) for row in rows]

@router.get('/{id}', response_model=Transacao)
def get_transacao(id: int, db: DataBase = Depends(get_db)):
    row = db.execute_one(
        "SELECT id, conta_id, categoria_id, valor, data, descricao, ativo FROM transacao WHERE id = %s",
        (id,)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Transacao não encontrada')
    return dict(row)

@router.post('/', response_model=Transacao, status_code=201)
def create_transacao(payload: TransacaoCreate, db: DataBase = Depends(get_db)):
    if payload.valor <= 0:
        raise HTTPException(status_code=400, detail='valor deve ser maior que zero')
    
    # Verificar se conta existe e está ativa
    conta = db.execute_one("SELECT id, ativo FROM conta WHERE id = %s", (payload.conta_id,))
    if not conta:
        raise HTTPException(status_code=404, detail='Conta não encontrada')
    if not conta['ativo']:
        raise HTTPException(status_code=400, detail='Conta está desativada')
    
    # Verificar se categoria existe e está ativa
    categoria = db.execute_one("SELECT id, ativo FROM categoria WHERE id = %s", (payload.categoria_id,))
    if not categoria:
        raise HTTPException(status_code=404, detail='Categoria não encontrada')
    if not categoria['ativo']:
        raise HTTPException(status_code=400, detail='Categoria está desativada')
    
    row = db.commit(
        "INSERT INTO transacao (conta_id, categoria_id, valor, data, descricao, ativo) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, conta_id, categoria_id, valor, data, descricao, ativo",
        (payload.conta_id, payload.categoria_id, payload.valor, payload.data, payload.descricao, True)
    )
    return dict(row)

@router.put('/{id}', response_model=Transacao)
def update_transacao(id: int, payload: TransacaoUpdate, db: DataBase = Depends(get_db)):
    # Verificar se a transação existe
    transacao = db.execute_one("SELECT id FROM transacao WHERE id = %s", (id,))
    if not transacao:
        raise HTTPException(status_code=404, detail='Transacao não encontrada')
    
    # Construir query de atualização dinamicamente
    updates = []
    params = []
    
    if payload.conta_id is not None:
        # Verificar se conta existe e está ativa
        conta = db.execute_one("SELECT id, ativo FROM conta WHERE id = %s", (payload.conta_id,))
        if not conta:
            raise HTTPException(status_code=404, detail='Conta não encontrada')
        if not conta['ativo']:
            raise HTTPException(status_code=400, detail='Conta está desativada')
        updates.append("conta_id = %s")
        params.append(payload.conta_id)
    
    if payload.categoria_id is not None:
        # Verificar se categoria existe e está ativa
        categoria = db.execute_one("SELECT id, ativo FROM categoria WHERE id = %s", (payload.categoria_id,))
        if not categoria:
            raise HTTPException(status_code=404, detail='Categoria não encontrada')
        if not categoria['ativo']:
            raise HTTPException(status_code=400, detail='Categoria está desativada')
        updates.append("categoria_id = %s")
        params.append(payload.categoria_id)
    
    if payload.valor is not None:
        if payload.valor <= 0:
            raise HTTPException(status_code=400, detail='valor deve ser maior que zero')
        updates.append("valor = %s")
        params.append(payload.valor)
    
    if payload.data is not None:
        updates.append("data = %s")
        params.append(payload.data)
    
    if payload.descricao is not None:
        updates.append("descricao = %s")
        params.append(payload.descricao)
    
    if not updates:
        # Se não há atualizações, retornar a transação atual
        return get_transacao(id, db)
    
    params.append(id)
    query = f"UPDATE transacao SET {', '.join(updates)} WHERE id = %s RETURNING id, conta_id, categoria_id, valor, data, descricao, ativo"
    
    row = db.commit(query, tuple(params))
    return dict(row)

@router.patch('/{id}/desativar', status_code=204)
def desativar_transacao(id: int, db: DataBase = Depends(get_db)):
    row = db.commit(
        "UPDATE transacao SET ativo = %s WHERE id = %s RETURNING id",
        (False, id)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Transacao não encontrada')
    return None
=======

@router.get("/", response_model=List[Transacao])
def list_transacoes(db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT id, conta_id, categoria_id, valor, data, descricao
            FROM transacao
            ORDER BY id
        """)
        rows = cur.fetchall()
    return rows


@router.get("/{id}", response_model=Transacao)
def get_transacao(id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            SELECT id, conta_id, categoria_id, valor, data, descricao
            FROM transacao
            WHERE id = %s
        """, (id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return row


@router.post("/", response_model=Transacao)
def create_transacao(payload: TransacaoCreate, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            INSERT INTO transacao (conta_id, categoria_id, valor, data, descricao)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, conta_id, categoria_id, valor, data, descricao
        """, (payload.conta_id, payload.categoria_id, payload.valor, payload.data, payload.descricao))
        row = cur.fetchone()
        db.commit()
    return row


@router.put("/{id}", response_model=Transacao)
def update_transacao(id: int, payload: TransacaoCreate, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""
            UPDATE transacao
            SET conta_id = %s, categoria_id = %s, valor = %s, data = %s, descricao = %s
            WHERE id = %s
            RETURNING id, conta_id, categoria_id, valor, data, descricao
        """, (payload.conta_id, payload.categoria_id, payload.valor, payload.data, payload.descricao, id))
        row = cur.fetchone()
        db.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return row


@router.delete("/{id}")
def delete_transacao(id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("DELETE FROM transacao WHERE id = %s RETURNING id", (id,))
        row = cur.fetchone()
        db.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return {"detail": "Transação deletada com sucesso"}
>>>>>>> 8df36cda30eeeaec837af4a9e0f7d54ef24e57c6
