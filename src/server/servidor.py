from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery

# Importa as funções de registro dos nossos novos módulos
from .tools import register_tools
from .prompts import register_prompts
from .resources import register_resources

@smithery.server()
def create_server():
    """
    Cria a instância do servidor e registra todas as suas funcionalidades
    importando de outros módulos.
    """
    print("Iniciando a criação do servidor MCP...")
    mcp = FastMCP("MeuServidorMCP", stateless_http=True)

    # Chama cada função de registro para adicionar as funcionalidades ao servidor
    register_resources(mcp)
    register_prompts(mcp)
    register_tools(mcp)
    
    print("Criação do servidor MCP concluída.")
    return mcp