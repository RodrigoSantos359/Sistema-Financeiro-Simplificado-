from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from core.db import get_db, DataBase
from modules.pagamento.schemas import PagamentoCreate, PagamentoUpdate, Pagamento

router = APIRouter(prefix='/pagamentos', tags=['pagamentos'])

@router.get('/', response_model=List[Pagamento])
def list_pagamentos(
    transacao_id: Optional[int] = Query(None, description="Filtrar por transação"),
    status: Optional[str] = Query(None, description="Filtrar por status (pago/pendente/cancelado)"),
    data_ini: Optional[datetime] = Query(None, description="Data inicial (ISO 8601)"),
    data_fim: Optional[datetime] = Query(None, description="Data final (ISO 8601)"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    db: DataBase = Depends(get_db)
):
    query = "SELECT id, transacao_id, status, data_pagamento, ativo FROM pagamento WHERE 1=1"
    params = []
    
    if transacao_id:
        query += " AND transacao_id = %s"
        params.append(transacao_id)
    
    if status:
        if status not in ('pago', 'pendente', 'cancelado'):
            raise HTTPException(status_code=400, detail='status deve ser pago, pendente ou cancelado')
        query += " AND status = %s"
        params.append(status)
    
    if data_ini:
        query += " AND data_pagamento >= %s"
        params.append(data_ini)
    
    if data_fim:
        query += " AND data_pagamento <= %s"
        params.append(data_fim)
    
    if ativo is not None:
        query += " AND ativo = %s"
        params.append(ativo)
    
    query += " ORDER BY id"
    
    rows = db.execute(query, tuple(params) if params else None)
    return [dict(row) for row in rows]

@router.get('/{id}', response_model=Pagamento)
def get_pagamento(id: int, db: DataBase = Depends(get_db)):
    row = db.execute_one(
        "SELECT id, transacao_id, status, data_pagamento, ativo FROM pagamento WHERE id = %s",
        (id,)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    return dict(row)

@router.post('/', response_model=Pagamento, status_code=201)
def create_pagamento(payload: PagamentoCreate, db: DataBase = Depends(get_db)):
    if payload.status not in ('pago', 'pendente', 'cancelado'):
        raise HTTPException(status_code=400, detail='status deve ser pago, pendente ou cancelado')
    
    # Verificar se transação existe e está ativa
    transacao = db.execute_one("SELECT id, ativo, data FROM transacao WHERE id = %s", (payload.transacao_id,))
    if not transacao:
        raise HTTPException(status_code=404, detail='Transacao não encontrada')
    if not transacao['ativo']:
        raise HTTPException(status_code=400, detail='Transacao está desativada')
    
    # Validar data_pagamento não pode ser anterior à data da transação
    if payload.data_pagamento and transacao['data']:
        if payload.data_pagamento < transacao['data']:
            raise HTTPException(status_code=400, detail='data_pagamento não pode ser anterior à data da transação')
    
    row = db.commit(
        "INSERT INTO pagamento (transacao_id, status, data_pagamento, ativo) VALUES (%s, %s, %s, %s) RETURNING id, transacao_id, status, data_pagamento, ativo",
        (payload.transacao_id, payload.status, payload.data_pagamento, True)
    )
    return dict(row)

@router.put('/{id}', response_model=Pagamento)
def update_pagamento(id: int, payload: PagamentoUpdate, db: DataBase = Depends(get_db)):
    # Verificar se o pagamento existe
    pagamento = db.execute_one("SELECT id FROM pagamento WHERE id = %s", (id,))
    if not pagamento:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    
    # Construir query de atualização dinamicamente
    updates = []
    params = []
    
    if payload.transacao_id is not None:
        # Verificar se transação existe e está ativa
        transacao = db.execute_one("SELECT id, ativo, data FROM transacao WHERE id = %s", (payload.transacao_id,))
        if not transacao:
            raise HTTPException(status_code=404, detail='Transacao não encontrada')
        if not transacao['ativo']:
            raise HTTPException(status_code=400, detail='Transacao está desativada')
        updates.append("transacao_id = %s")
        params.append(payload.transacao_id)
    
    if payload.status is not None:
        if payload.status not in ('pago', 'pendente', 'cancelado'):
            raise HTTPException(status_code=400, detail='status deve ser pago, pendente ou cancelado')
        updates.append("status = %s")
        params.append(payload.status)
    
    if payload.data_pagamento is not None:
        # Se mudou transacao_id, buscar a nova transação para validar data
        transacao_id = payload.transacao_id if payload.transacao_id else None
        if not transacao_id:
            # Buscar transacao_id atual
            pagamento_atual = db.execute_one("SELECT transacao_id FROM pagamento WHERE id = %s", (id,))
            transacao_id = pagamento_atual['transacao_id']
        
        transacao = db.execute_one("SELECT data FROM transacao WHERE id = %s", (transacao_id,))
        if transacao and payload.data_pagamento < transacao['data']:
            raise HTTPException(status_code=400, detail='data_pagamento não pode ser anterior à data da transação')
        
        updates.append("data_pagamento = %s")
        params.append(payload.data_pagamento)
    
    if not updates:
        # Se não há atualizações, retornar o pagamento atual
        return get_pagamento(id, db)
    
    params.append(id)
    query = f"UPDATE pagamento SET {', '.join(updates)} WHERE id = %s RETURNING id, transacao_id, status, data_pagamento, ativo"
    
    row = db.commit(query, tuple(params))
    return dict(row)

@router.patch('/{id}/desativar', status_code=204)
def desativar_pagamento(id: int, db: DataBase = Depends(get_db)):
    row = db.commit(
        "UPDATE pagamento SET ativo = %s WHERE id = %s RETURNING id",
        (False, id)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    return None
