<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from core.db import get_db, DataBase
from modules.conta.schemas import ContaCreate, ContaUpdate, Conta
=======
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from core.db import get_db
from modules.conta.schemas import ContaCreate, Conta
>>>>>>> 8df36cda30eeeaec837af4a9e0f7d54ef24e57c6

router = APIRouter(prefix="/contas", tags=["contas"])

<<<<<<< HEAD
@router.get('/', response_model=List[Conta])
def list_contas(
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    db: DataBase = Depends(get_db)
):
    query = "SELECT id, nome, saldo_inicial, ativo FROM conta WHERE 1=1"
    params = []
    
    if nome:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome}%")
    
    if ativo is not None:
        query += " AND ativo = %s"
        params.append(ativo)
    
    query += " ORDER BY id"
    
    rows = db.execute(query, tuple(params) if params else None)
    return [dict(row) for row in rows]

@router.get('/{id}', response_model=Conta)
def get_conta(id: int, db: DataBase = Depends(get_db)):
    row = db.execute_one(
        "SELECT id, nome, saldo_inicial, ativo FROM conta WHERE id = %s",
        (id,)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Conta não encontrada')
    return dict(row)

@router.post('/', response_model=Conta, status_code=201)
def create_conta(payload: ContaCreate, db: DataBase = Depends(get_db)):
    if payload.saldo_inicial < 0:
        raise HTTPException(status_code=400, detail='saldo_inicial deve ser maior ou igual a zero')
    
    row = db.commit(
        "INSERT INTO conta (nome, saldo_inicial, ativo) VALUES (%s, %s, %s) RETURNING id, nome, saldo_inicial, ativo",
        (payload.nome, payload.saldo_inicial, True)
    )
    return dict(row)

@router.put('/{id}', response_model=Conta)
def update_conta(id: int, payload: ContaUpdate, db: DataBase = Depends(get_db)):
    # Verificar se a conta existe
    conta = db.execute_one("SELECT id FROM conta WHERE id = %s", (id,))
    if not conta:
        raise HTTPException(status_code=404, detail='Conta não encontrada')
    
    # Construir query de atualização dinamicamente
    updates = []
    params = []
    
    if payload.nome is not None:
        updates.append("nome = %s")
        params.append(payload.nome)
    
    if payload.saldo_inicial is not None:
        if payload.saldo_inicial < 0:
            raise HTTPException(status_code=400, detail='saldo_inicial deve ser maior ou igual a zero')
        updates.append("saldo_inicial = %s")
        params.append(payload.saldo_inicial)
    
    if not updates:
        # Se não há atualizações, retornar a conta atual
        return get_conta(id, db)
    
    params.append(id)
    query = f"UPDATE conta SET {', '.join(updates)} WHERE id = %s RETURNING id, nome, saldo_inicial, ativo"
    
    row = db.commit(query, tuple(params))
    return dict(row)

@router.patch('/{id}/desativar', status_code=204)
def desativar_conta(id: int, db: DataBase = Depends(get_db)):
    row = db.commit(
        "UPDATE conta SET ativo = %s WHERE id = %s RETURNING id",
        (False, id)
    )
    if not row:
        raise HTTPException(status_code=404, detail='Conta não encontrada')
    return None
=======
@router.get("/", response_model=List[Conta])
def list_contas(db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT id, nome, saldo_inicial FROM conta ORDER BY id")
        rows = cur.fetchall()
    return rows

@router.get("/{id}", response_model=Conta)
def get_conta(id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT id, nome, saldo_inicial FROM conta WHERE id = %s", (id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return row

@router.post("/", response_model=Conta)
def create_conta(payload: ContaCreate, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO conta (nome, saldo_inicial) VALUES (%s, %s) RETURNING id, nome, saldo_inicial",
            (payload.nome, payload.saldo_inicial)
        )
        row = cur.fetchone()
        db.commit()
    return row

@router.put("/{id}", response_model=Conta)
def update_conta(id: int, payload: ContaCreate, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            "UPDATE conta SET nome = %s, saldo_inicial = %s WHERE id = %s RETURNING id, nome, saldo_inicial",
            (payload.nome, payload.saldo_inicial, id)
        )
        row = cur.fetchone()
        db.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return row

@router.delete("/{id}")
def delete_conta(id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("DELETE FROM conta WHERE id = %s RETURNING id", (id,))
        row = cur.fetchone()
        db.commit()
    if not row:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"detail": "Conta deletada com sucesso"}
>>>>>>> 8df36cda30eeeaec837af4a9e0f7d54ef24e57c6
