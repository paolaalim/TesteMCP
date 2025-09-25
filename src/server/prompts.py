from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

def register_prompts(mcp: FastMCP):
    """Registra todos os prompts do servidor."""

    @mcp.prompt()
    def debug_error(error: str) -> list[base.Message]:
        """Inicia uma conversa para ajudar a depurar um erro."""
        return [
            base.UserMessage(f"Estou com este erro: {error}"),
            base.AssistantMessage("Entendido. O que já tentou fazer para resolver?"),
        ]

    print("-> Prompts registrados.")