import os
import google.generativeai as genai

# pip install -q -U google-generativeai

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

GEMINI_API_KEY = os.getenv('secret_gemini')
genai.configure(api_key=GEMINI_API_KEY)

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    "Escreva uma história em uma frase sobre uma princesa em um mundo de fantasia"
)
print(response.text)

response = model.generate_content(
    "Escreva uma história em uma frase sobre uma princesa em um mundo de fantasia",
    generation_config={"temperature": 1.5,"max_output_tokens": 100},
    safety_settings=[{"category":'HARM_CATEGORY_HATE_SPEECH','threshold':3}]
)
print(response.text)

# * top_p: Aqui você consegue controlar a seleção das palavras que serão utilizadas. Exemplo: top_p = 0.9 Considera só palavras até chegar em 90% de probabilidade acumulada.
# 0.1 a 0.3: Considera só as opções mais seguras
# 0.7 a 0.9: Considera várias opções
# 1: Considera todas as opções
# * top_k: Aqui conseguimos fazer a IA focar nas melhores palavras. Esse parâmetro limita o número de palavras que ela pode considerar.
# 1: Sempre escolhe a palavra mais provável
# 40: Escolhe entre as 40 palavras mais prováveis
# 100: Mais opções → mais diversidade
# * safety_gettings: Define o nível de moderação de conteúdo sensível, ou seja, serve para controlar o que a IA pode ou não falar.
# 1 > Muito sensível (censura rápido)
# 4 > Mais permissivo (deixa passar mais coisas)