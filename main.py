# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Usuario(BaseModel):
#     nome: str

# usuarios = []

# @app.get("/usuarios")
# def lista_usuarios():
#     return usuarios

# @app.post("/usuarios")
# def cadastrar_usuario(usuario: Usuario):
#     novo_id = 1
#     if len(usuarios) > 0:
#         novo_id = usuario[-1]["id"] + 1

#     novo_usuario = {"id": novo_id, "nome": usuario.nome}
#     usuarios.append(novo_usuario)
#     return novo_usuario

# @app.put("/usuarios/{id}")
# def atualizar_usuario(id: int, usuario: Usuario):
#     for u in usuarios:
#         if u["id"] == id:
#             u["nome"] = usuario.nome
#     raise HTTPException(status_code=404, detail="Usuário não encontrado")

# @app.delete("/usuarios/{id}")
# def excluir_usuarios(id: int):
#     for u in usuarios:
#         if u["id"] == id:
#             usuarios.remove(u)
#             return {"message": "Usuário excluído com sucesso."}
#     raise HTTPException(status_code=404, detail="Usuário não encontrado")

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
 
 
# app = FastAPI()
 
 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
 
 
# class Usuario(BaseModel):
#     nome: str
 
 
# usuarios = [
#     {"id": 1, "nome": "Ana"},
#     {"id": 2, "nome": "Carlos"}
# ]
 
 
# @app.get("/usuarios")
# def listar_usuarios():
 
#     return usuarios
 
 
# @app.post("/usuarios")
# def cadastrar_usuario(usuario: Usuario):
 
#     novo_id = 1
 
#     if len(usuarios) > 0:
#         novo_id = usuarios[-1]["id"] + 1
 
#     novo_usuario = {
#         "id": novo_id,
#         "nome": usuario.nome
#     }
 
#     usuarios.append(novo_usuario)
 
#     return novo_usuario
 
 
# @app.put("/usuarios/{id}")
# def atualizar_usuario(id: int, usuario: Usuario):
 
#     for item in usuarios:
 
#         if item["id"] == id:
 
#             item["nome"] = usuario.nome
 
#             return item
 
#     raise HTTPException(
#         status_code=404,
#         detail="Usuário não encontrado"
#     )
 
 
# @app.delete("/usuarios/{id}")
# def excluir_usuario(id: int):
 
#     for item in usuarios:
 
#         if item["id"] == id:
 
#             usuarios.remove(item)
 
#             return {
#                 "mensagem": "Usuário excluído com sucesso"
#             }
 
#     raise HTTPException(
#         status_code=404,
#         detail="Usuário não encontrado"
#     )

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase: Client = create_client(
    supabase_url=os.getenv("SUABASE_URL"),
    supabase_key=os.getenv("SUABASE_KEY"),
)

class Usuario(BaseModel):
    nome: str

@app.get("/usuarios")
def listar_usuarios():
    response = supabase.table("usuarios").slect("*").order("id", desc=False).execute()
    return response.data

@app.post("/usuarios")
def cadastrar_usuario(usuario: Usuario):
    resposta = supabase.table("usuarios").insert({"nome":usuario.nome}).execute()
    return resposta.data[0]

@app.put("/usuarios/{id}")
def atualizar_usuario(i: int, usuario: Usuario):
    response = supabase.table("usuarios").update({"nome": usuario.nome}).eq("id", id).execute()

    if len(response.data) == 0:
        raise HTTPException(status_code=404,
                            detail="Usuário não encontrado")
    return response.data[0]

@app.delete("/usuarios/{id}")
def excluir_usuario(id: int):
    response = supabase.table(
        "usuarios").delete().eq("id", id).execute()

    if len(response.data) ==0:
        raise HTTPException(status_code=404,
                            detail="Usuário não encontrado")
    return {"message": "Usuário excluído com sucesso"}