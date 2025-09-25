import re
from collections import Counter
import asyncio
from random import randint
from mcp.server.fastmcp import FastMCP, Context

# A lista de stopwords pode ficar aqui, junto com as ferramentas que a utilizam.
stopwords_pt = [
    'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com', 
    'não', 'uma', 'os', 'no', 'na', 'por', 'mais', 'as', 'dos', 'como', 
    'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua'
]

def register_tools(mcp: FastMCP):
    """Registra todas as ferramentas (tools) do servidor."""

    @mcp.tool()
    def contar_frequencia_palavras(texto: str) -> str:
        """Conta a frequência das palavras importantes num texto, ignorando artigos e preposições."""
        palavras = re.findall(r'\b\w+\b', texto.lower())
        palavras_filtradas = [p for p in palavras if p not in stopwords_pt]
        if not palavras_filtradas:
            return "Nenhuma palavra significativa foi encontrada."
        contagem = Counter(palavras_filtradas)
        return ", ".join([f"{p}: {f}" for p, f in contagem.most_common()])

    @mcp.tool()
    def obter_previsao_tempo(cidade: str) -> str:
        """Retorna a previsão do tempo simulada para uma cidade específica."""
        temperatura_simulada = randint(15, 30)
        condicoes = ["Ensolarado", "Parcialmente Nublado", "Chuvoso"]
        condicao_simulada = condicoes[randint(0, len(condicoes)-1)]
        return f"A previsão do tempo para {cidade} é: {temperatura_simulada}°C e {condicao_simulada}."

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

    print("-> Tools registradas.")