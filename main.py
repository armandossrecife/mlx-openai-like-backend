from openai import OpenAI

MODELO_LLM = "mlx-community/Llama-3.2-3B-Instruct-4bit"
#MODELO_LLM = "mlx-community/Qwen3-4B-Instruct-2507-4bit"

print("Teste com a biblioteca OpenAI para conectar ao MLX")
print("Conectando ao servidor MLX...")
try:
    # Aponta para o seu servidor local
    client = OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="nao-necessaria-pois-roda-localmente" 
    )
except Exception as e:
    print("Erro ao conectar ao servidor MLX:", e)
    exit(1)

try:
    print("Enviando solicitação de conclusão de chat ao MLX...")
    response = client.chat.completions.create(
        model=MODELO_LLM,
        messages=[
            {"role": "system", "content": "Você é cientista da computação especialista em IA Generativa."},
            {"role": "user", "content": "Qual a vantagem de usar MLX no Mac? Lembre-se que o MLX que eu me refiro é um 'Python package for generating text and fine-tuning large language models on Apple silicon'"}
        ],
        stream=True  # O MLX suporta streaming (resposta token a token)
    )

    print("Resposta do MLX:")
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
except Exception as e:
    print("Erro ao obter a resposta do MLX:", e)