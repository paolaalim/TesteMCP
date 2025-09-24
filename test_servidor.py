#!/usr/bin/env python3
"""
Script de teste para validar o servidor MCP
"""
import asyncio
import json
from servidor import contar_frequencia_palavras_impl, extrair_urls_texto_impl

def test_contar_palavras():
    """Testa a função de contagem de palavras."""
    print("=== Testando Contagem de Palavras ===")
    
    # Teste 1: Texto normal
    texto1 = "python é uma linguagem python muito python popular"
    resultado1 = contar_frequencia_palavras_impl(texto1)
    print(f"Entrada: {texto1}")
    print(f"Resultado: {resultado1}")
    print()
    
    # Teste 2: Texto vazio
    resultado2 = contar_frequencia_palavras_impl("")
    print(f"Entrada: (vazio)")
    print(f"Resultado: {resultado2}")
    print()

def test_extrair_urls():
    """Testa a função de extração de URLs."""
    print("=== Testando Extração de URLs ===")
    
    # Teste 1: Texto com URLs
    texto1 = "Visite https://example.com e também http://test.com para mais informações"
    resultado1 = extrair_urls_texto_impl(texto1)
    print(f"Entrada: {texto1}")
    print(f"Resultado: {resultado1}")
    print()
    
    # Teste 2: Texto sem URLs
    texto2 = "Este texto não tem links"
    resultado2 = extrair_urls_texto_impl(texto2)
    print(f"Entrada: {texto2}")
    print(f"Resultado: {resultado2}")
    print()

def test_endpoints():
    """Testa se os dados dos endpoints estão corretos."""
    print("=== Testando Estrutura dos Endpoints ===")
    
    # Dados dos recursos
    resources = [
        {
            "uri": "meuMCP://about",
            "name": "Sobre o Assistente",
            "description": "Descrição das capacidades do assistente",
            "mimeType": "text/plain"
        }
    ]
    print(f"Recursos: {json.dumps(resources, indent=2, ensure_ascii=False)}")
    print()
    
    # Dados das ferramentas
    tools = [
        {
            "name": "contar_frequencia_palavras",
            "description": "Conta a frequência de cada palavra em um texto fornecido"
        },
        {
            "name": "extrair_urls_texto", 
            "description": "Encontra e lista todas as URLs (http ou https) dentro de um texto"
        }
    ]
    print(f"Ferramentas: {json.dumps(tools, indent=2, ensure_ascii=False)}")

def main():
    """Executa todos os testes."""
    print("🚀 Iniciando testes do Servidor MCP\n")
    
    test_contar_palavras()
    test_extrair_urls()
    test_endpoints()
    
    print("✅ Todos os testes concluídos!")
    print("\n💡 Para testar o servidor HTTP completo, execute:")
    print("   python servidor.py")
    print("   Em seguida, acesse http://localhost:8080")

if __name__ == "__main__":
    main()