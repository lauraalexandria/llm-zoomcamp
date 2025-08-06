import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

# Primeiro teste

response = client.responses.create(
    model="gpt-4.1",
    input="Escreva uma história em uma frase sobre uma princesa em um mundo de fantasia"
)

print(response.output_text)

# instructions é um argumento para definir a personalidae/comportamento da IA

response = client.responses.create(
    model="gpt-4.1",
    instructions="Escreva como o Bob Esponja",
    input="Escreva uma história em uma frase sobre uma princesa em um mundo de fantasia")

print(response.output_text)

# * Temperatura (0 a 2): Define a criatividade da resposta. Use valores baixos para respostas técnicas e valores altos para gerar ideias criativas. 
# * max_tokens: Limita quantas palavras a IA pode escrever. Use valores pequenos se quiser respostas curtas, e maiores para explicações completas. max_tokens = 100 → aprox. 75 palavras
# * frequency_penalty=0: Utilizado para controlar repetições na resposta