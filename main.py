from openai import OpenAI
from app.core.config import settings

print("Teste com a biblioteca OpenAI para conectar ao LLM_SERVER")
print("Conectando ao servidor LLM_SERVER...")
try:
    # Aponta para o seu servidor local
    client = OpenAI(
        base_url=settings.LLM_SERVER_BASE_URL,
        api_key="nao-necessaria-pois-roda-localmente" 
    )
except Exception as e:
    print("Erro ao conectar ao servidor LLM_SERVER:", e)
    exit(1)

try:
    print("Enviando solicitação de conclusão de chat ao LLM_SERVER...")
    response = client.chat.completions.create(
        model=settings.MODELO_LLM,
        messages=[
            {"role": "system", "content": "Você é cientista da computação especialista em IA Generativa."},
            {"role": "user", "content": "Qual a vantagem de usar LLM_SERVER no Mac? Lembre-se que o LLM_SERVER que eu me refiro é um 'Python package for generating text and fine-tuning large language models on Apple silicon'"}
        ],
        stream=True  # O LLM_SERVER suporta streaming (resposta token a token)
    )

    print("Resposta do LLM_SERVER:")
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
except Exception as e:
    print("Erro ao obter a resposta do LLM_SERVER:", e)