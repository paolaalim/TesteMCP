from mcp.server.fastmcp import FastMCP

def register_resources(mcp: FastMCP):
    """Registra todos os resources do servidor."""

    @mcp.resource("meuMCP://about")
    def get_assistant_capabilities() -> str:
        """Descreve as principais ferramentas e o propósito deste assistente."""
        return """
        Eu sou um assistente de exemplo. Minhas ferramentas são:
        1. Contar Frequência de Palavras (agora mais inteligente!)
        2. Extrair URLs
        3. Registrar Logs
        4. Obter Previsão do Tempo (nova!)
        """.strip()
    
    print("-> Resources registrados.")