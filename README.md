# Instruções Gerais

## Dependências

```bash
uv add openai
```

## Teste de Execução da Aplicação OpenAI Like

```bash
uv run main.py
```

Se não mostrar error e responder a pergunta corretamente o ambiente está ok.

# Instruções da Aplicação Backend

## Dependências

```bash
uv add fastapi uvicorn sqlalchemy pydantic-settings python-jose "bcrypt==4.0.1" passlib httpx
uv add "pydantic[email]"
```

```bash
cd api-openai
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```