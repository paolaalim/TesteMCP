# servidor.py - Servidor MCP para deploy no Smithery
import re
import json
import asyncio
from collections import Counter
from typing import Any, Dict, List

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# --- Dados do servidor MCP ---
SERVER_INFO = {
    "name": "MeuServidorMCP",
    "version": "1.0.0",
    "description": "Servidor MCP de demonstração com análise de texto"
}

# --- RESOURCES ---
async def list_resources(request):
    """Lista todos os recursos disponíveis."""
    resources = [
        {
            "uri": "meuMCP://about",
            "name": "Sobre o Assistente",
            "description": "Descrição das capacidades do assistente",
            "mimeType": "text/plain"
        }
    ]
    return JSONResponse({"resources": resources})

async def read_resource(request):
    """Lê o conteúdo de um recurso específico."""
    uri = request.query_params.get("uri")
    
    if uri == "meuMCP://about":
        content = """
Eu sou um assistente de exemplo baseado no servidor 'MeuServidorMCP'. 
Minhas principais capacidades são:
1. **Contar Frequência de Palavras:** Analisar um texto e contar quantas vezes cada palavra aparece.
2. **Extrair URLs:** Encontrar links (http/https) dentro de um texto.

Use-me para processar textos e análise de conteúdo!
"""
        return JSONResponse({
            "contents": [
                {
                    "type": "text",
                    "text": content.strip()
                }
            ]
        })
    else:
        return JSONResponse({"error": f"Recurso não encontrado: {uri}"}, status_code=404)

# --- TOOLS ---
async def list_tools(request):
    """Lista todas as ferramentas disponíveis."""
    tools = [
        {
            "name": "contar_frequencia_palavras",
            "description": "Conta a frequência de cada palavra em um texto fornecido",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "texto": {
                        "type": "string",
                        "description": "O texto para análise de frequência de palavras"
                    }
                },
                "required": ["texto"]
            }
        },
        {
            "name": "extrair_urls_texto", 
            "description": "Encontra e lista todas as URLs (http ou https) dentro de um texto",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "texto": {
                        "type": "string",
                        "description": "O texto para extração de URLs"
                    }
                },
                "required": ["texto"]
            }
        }
    ]
    return JSONResponse({"tools": tools})

def contar_frequencia_palavras_impl(texto: str) -> str:
    """Implementação da contagem de frequência de palavras."""
    print(f"-> Ferramenta 'contar_frequencia_palavras' chamada com texto: '{texto[:50]}...'")
    
    if not texto:
        return "Nenhum texto fornecido para análise."
    
    try:
        palavras = re.findall(r'\b\w+\b', texto.lower())
        if not palavras:
            return "Nenhuma palavra encontrada no texto."
        
        contagem = Counter(palavras)
        resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
        resultado = f"Frequência de palavras: {resultado_str}"
        print(f"   Resultado: {resultado}")
        return resultado
        
    except Exception as e:
        erro = f"Ocorreu um erro inesperado ao contar palavras: {e}"
        print(f"   Erro: {erro}")
        return erro

def extrair_urls_texto_impl(texto: str) -> str:
    """Implementação da extração de URLs."""
    print(f"-> Ferramenta 'extrair_urls_texto' chamada com texto: '{texto[:50]}...'")
    
    if not texto:
        return "Nenhum texto fornecido para extrair URLs."
    
    try:
        urls_encontradas = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', texto)
        if urls_encontradas:
            resultado = f"URLs encontradas ({len(urls_encontradas)}): " + ", ".join(urls_encontradas)
        else:
            resultado = "Nenhuma URL encontrada no texto."
        print(f"   Resultado: {resultado}")
        return resultado
        
    except Exception as e:
        erro = f"Ocorreu um erro inesperado ao extrair URLs: {e}"
        print(f"   Erro: {erro}")
        return erro

async def call_tool(request):
    """Executa uma ferramenta específica."""
    body = await request.json()
    name = body.get("name")
    arguments = body.get("arguments", {})
    
    if name == "contar_frequencia_palavras":
        texto = arguments.get("texto", "")
        resultado = contar_frequencia_palavras_impl(texto)
        return JSONResponse({
            "content": [
                {
                    "type": "text",
                    "text": resultado
                }
            ]
        })
    
    elif name == "extrair_urls_texto":
        texto = arguments.get("texto", "")
        resultado = extrair_urls_texto_impl(texto)
        return JSONResponse({
            "content": [
                {
                    "type": "text", 
                    "text": resultado
                }
            ]
        })
    
    else:
        return JSONResponse({"error": f"Ferramenta desconhecida: {name}"}, status_code=400)

# --- Info endpoint ---
async def server_info(request):
    """Retorna informações sobre o servidor."""
    return JSONResponse(SERVER_INFO)

async def health_check(request):
    """Endpoint de verificação de saúde."""
    return JSONResponse({"status": "ok", "server": SERVER_INFO["name"]})

# --- Configuração da aplicação Starlette ---
routes = [
    Route("/", health_check, methods=["GET"]),
    Route("/health", health_check, methods=["GET"]),
    Route("/info", server_info, methods=["GET"]),
    Route("/resources", list_resources, methods=["GET"]),
    Route("/resources/read", read_resource, methods=["GET"]),
    Route("/tools", list_tools, methods=["GET"]),
    Route("/tools/call", call_tool, methods=["POST"]),
]

app = Starlette(routes=routes)

# --- Função principal ---
if __name__ == "__main__":
    print(f"Iniciando servidor {SERVER_INFO['name']} v{SERVER_INFO['version']}")
    uvicorn.run(app, host="0.0.0.0", port=8080)

