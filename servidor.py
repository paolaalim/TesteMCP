# --- Imports ---
import re
from collections import Counter
import asyncio
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from smithery.decorators import smithery # Importar o decorator obrigatório

# O decorator @smithery.server() marca esta função como o ponto de entrada
@smithery.server()
def create_server():
    """
    Cria, configura e retorna a instância do servidor FastMCP.
    É esta função que o Smithery vai chamar para iniciar o servidor.
    """
    # 1. Inicialize o Servidor dentro da função
    mcp = FastMCP("MeuServidorMCP", stateless_http=True)
    print(f"Servidor MCP '{mcp.name}' está a ser criado.")

    # --- RESOURCES ---
    @mcp.resource("meuMCP://about")
    def get_assistant_capabilities() -> str:
        """Descreve as principais ferramentas e o propósito deste assistente."""
        return """
        Eu sou um assistente de exemplo. As minhas ferramentas são:
        1. Contar Frequência de Palavras
        2. Extrair URLs
        3. Registrar Logs
        """.strip()

    # --- FERRAMENTAS (Tools) ---
    @mcp.tool()
    def contar_frequencia_palavras(texto: str) -> str:
        """Conta a frequência de cada palavra num texto fornecido."""
        palavras = re.findall(r'\b\w+\b', texto.lower())
        if not palavras:
            return "Nenhuma palavra encontrada."
        contagem = Counter(palavras)
        return ", ".join([f"{p}: {f}" for p, f in contagem.most_common()])

    @mcp.tool()
    def extrair_urls_texto(texto: str) -> str:
        """Encontra e lista todas as URLs (http ou https) dentro de um texto."""
        urls = re.findall(r'http[s]?://\S+', texto)
        if not urls:
            return "Nenhuma URL encontrada."
        return f"URLs encontradas ({len(urls)}): " + ", ".join(urls)

    @mcp.tool()
    async def registrar_log_interno(mensagem: str, ctx: Context) -> str:
        """Registra uma mensagem nos logs internos do servidor."""
        await ctx.info(f"Log da ferramenta: {mensagem}")
        return f"Mensagem '{mensagem}' registrada."

    # --- PROMPTS ---
    @mcp.prompt()
    def debug_error(error: str) -> list[base.Message]:
        """Inicia uma conversa para ajudar a depurar um erro."""
        return [
            base.UserMessage(f"Estou com este erro: {error}"),
            base.AssistantMessage("Entendido. O que já tentou fazer para resolver?"),
        ]

    # 3. A função deve retornar a instância do servidor criada
    print("Criação do servidor MCP concluída.")
    return mcp
