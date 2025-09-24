[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/paolaalim-testemcp-badge.png)](https://mseep.ai/app/paolaalim-testemcp)

[![smithery badge](https://smithery.ai/badge/@paolaalim/testemcp)](https://smithery.ai/server/@paolaalim/testemcp)

# Servidor MCP de Demonstração

Este é um servidor MCP (Model Context Protocol) de demonstração que fornece ferramentas para análise de texto.

## Funcionalidades

- **Contar Frequência de Palavras**: Analisa um texto e conta a frequência de cada palavra
- **Extrair URLs**: Encontra e lista todas as URLs HTTP/HTTPS em um texto
- **Resource About**: Fornece informações sobre as capacidades do servidor

## Deploy no Smithery

### Pré-requisitos

1. Conta no [Smithery](https://smithery.ai)
2. Docker instalado (para teste local)
3. Git instalado

### Passos para Deploy

1. **Preparar o repositório**:
   ```bash
   git add .
   git commit -m "Preparar para deploy no Smithery"
   git push origin main
   ```

2. **No Smithery**:
   - Acesse o painel do Smithery
   - Clique em "New Server" ou "Add Server"
   - Conecte seu repositório GitHub
   - Selecione este repositório (`TesteMCP`)
   - O Smithery detectará automaticamente o arquivo `smithery.yaml`

3. **Configuração**:
   - O servidor será construído usando Docker
   - Porta exposta: 8080
   - Tipo: HTTP Server
   - A aplicação iniciará automaticamente

### Testando Localmente

Para testar o servidor localmente antes do deploy:

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python servidor.py
```

O servidor estará disponível em `http://localhost:8080`

### Endpoints Disponíveis

- `GET /` - Health check
- `GET /health` - Status do servidor
- `GET /info` - Informações do servidor
- `GET /resources` - Lista recursos disponíveis
- `GET /resources/read?uri=<uri>` - Lê um recurso específico
- `GET /tools` - Lista ferramentas disponíveis
- `POST /tools/call` - Executa uma ferramenta

### Estrutura do Projeto

```
├── servidor.py          # Servidor principal
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração Docker
├── smithery.yaml       # Configuração Smithery
└── README.md          # Este arquivo
```

### Exemplo de Uso das Ferramentas

#### Contar Frequência de Palavras
```json
POST /tools/call
{
    "name": "contar_frequencia_palavras",
    "arguments": {
        "texto": "python é uma linguagem python muito python"
    }
}
```

#### Extrair URLs
```json
POST /tools/call
{
    "name": "extrair_urls_texto", 
    "arguments": {
        "texto": "Visite https://example.com e http://test.com"
    }
}
```

## Suporte

Em caso de problemas com o deploy, verifique:

1. Se todos os arquivos estão commitados no repositório
2. Se o `smithery.yaml` está na raiz do projeto
3. Se as dependências no `requirements.txt` estão corretas
4. Os logs de build no painel do Smithery
