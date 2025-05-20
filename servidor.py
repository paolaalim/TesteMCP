import re
from collections import Counter
from mcp.server.fastmcp.prompts import base
from mcp.server.fastmcp import FastMCP, Context



# Inicialização do servidor
mcp = FastMCP("TesteServidorMCP")




# --- RESOURCES (Informações de Contexto para a IA) ---
@mcp.resource("TesteMCP://about")
def get_assistant_capabilities() -> str:
    """Descreve as principais ferramentas e o propósito deste assistente."""
    capacidades = """
    Eu sou um assistente do servidor 'TesteServidorMCP'. Posso executar as seguintes ações:
    1. Contar a frequência de palavras em um texto.
    2. Extrair URLs de um texto.
    3. Recomendar um site para aprender sobre IA.
    4. Registrar mensagens nos logs internos.
    """
    return capacidades.strip()





def minha_tool(ctx: Context):
    modelo = ctx.config.get("modelo", "claude-3")


# --- TOOLS (Ferramentas que a IA pode usar) ---

@mcp.tool()
def contar_frequencia_palavras(texto: str) -> str:
    """Conta a frequência de cada palavra em um texto fornecido."""
    palavras = re.findall(r'\b\w+\b', texto.lower())
    contagem = Counter(palavras)
    resultado = ", ".join(f"{palavra}: {freq}" for palavra, freq in contagem.items())
    return resultado

@mcp.tool()
def extrair_urls(texto: str) -> list[str]:
    """Extrai todas as URLs presentes no texto fornecido."""
    padrao_url = r"https?://[^\s]+"
    return re.findall(padrao_url, texto)

@mcp.tool()
def recomendar_site_ia() -> str:
    """Recomenda um site confiável para aprender Inteligência Artificial."""
    return "Recomendo o site https://www.coursera.org/learn/machine-learning ou https://huggingface.co/learn"

@mcp.tool()
def registrar_log_interno(mensagem: str, ctx: Context) -> str:
    """Grava uma mensagem de log no contexto interno do servidor."""
    ctx.info(f"[Log da Paola] {mensagem}")
    return "Mensagem registrada com sucesso no log interno."






@mcp.prompt("resumo_resultado")
def resumo_resultado() -> str:
    return "Resuma os resultados das ferramentas em frases curtas e compreensíveis para iniciantes."

@mcp.prompt("boasvindas")
def teste() -> str:
    return "Apresente um texto de boas vindas. "










# --- Execução do servidor ---
if __name__ == "__main__":
    mcp.run(transport="http", port=6277)
