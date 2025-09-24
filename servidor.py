# servidor.py (VERSÃO AJUSTADA PARA SMITHERY)

# --- Imports ---
import re
from collections import Counter
from mcp.server.fastmcp.prompts import base
from mcp.server.fastmcp import FastMCP, Context
import asyncio
from smithery.decorators import smithery # Importar o decorator
from pydantic import BaseModel # Para o schema de configuração

# O Smithery recomenda esta estrutura
@smithery.server()
def create_server():
    """Cria e retorna a instância do servidor FastMCP."""
    
    # 1. Inicialize o Servidor
    # O código que estava no escopo global agora fica dentro desta função
    mcp = FastMCP("MeuServidorMCP", stateless_http=True)
    print(f"Servidor MCP '{mcp.name}' inicializado.")

    # --- RESOURCES ---
    @mcp.resource("meuMCP://about")
    def get_assistant_capabilities() -> str:
        """Descreve as principais ferramentas e o propósito deste assistente."""
        print("-> Resource 'meuMCP://about' solicitado pelo cliente.")
        return """
        Eu sou um assistente de exemplo baseado no servidor 'MeuServidorMCP'. Minhas principais capacidades são:
        1.  **Contar Frequência de Palavras:** Analisar um texto e contar quantas vezes cada palavra aparece.
        2.  **Extrair URLs:** Encontrar links (http/https) dentro de um texto.
        3.  **Registrar Logs:** Posso registrar mensagens internamente.
        """.strip()

    # --- FERRAMENTAS (Tools) ---
    @mcp.tool()
    def contar_frequencia_palavras(texto: str) -> str:
        """Conta a frequência de cada palavra em um texto fornecido."""
        print(f"-> Ferramenta 'contar_frequencia_palavras' chamada...")
        if not texto: return "Nenhum texto fornecido para análise."
        palavras = re.findall(r'\b\w+\b', texto.lower())
        if not palavras: return "Nenhuma palavra encontrada no texto."
        contagem = Counter(palavras)
        resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
        return f"Frequência de palavras: {resultado_str}"

    @mcp.tool()
    def extrair_urls_texto(texto: str) -> str:
        """Encontra e lista todas as URLs (http ou https) dentro de um texto."""
        print(f"-> Ferramenta 'extrair_urls_texto' chamada...")
        urls_encontradas = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', texto)
        if urls_encontradas:
            return f"URLs encontradas ({len(urls_encontradas)}): " + ", ".join(urls_encontradas)
        else:
            return "Nenhuma URL encontrada no texto."

    @mcp.tool()
    async def registrar_log_interno(mensagem: str, ctx: Context) -> str:
        """Registra uma mensagem nos logs internos do servidor MCP."""
        print(f"-> Ferramenta 'registrar_log_interno' chamada...")
        await ctx.info(f"Log via ferramenta: {mensagem}")
        return f"Mensagem '{mensagem}' registrada nos logs."

    # --- PROMPTS ---
    @mcp.prompt()
    def debug_error(error: str) -> list[base.Message]:
        """Inicia uma conversa para ajudar a depurar um erro."""
        print(f"-> Prompt 'debug_error' iniciado com erro: {error}")
        return [
            base.UserMessage(f"Estou recebendo este erro:\n```\n{error}\n```"),
            base.AssistantMessage("Entendido. O que você já tentou fazer para resolver?"),
        ]

    # A função deve retornar a instância do servidor
    return mcp
