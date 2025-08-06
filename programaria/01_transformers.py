from transformers import pipeline

model_name = "pierreguillou/bert-base-cased-squad-v1.1-portuguese"

# Cria pipeline de QA
qa_pipeline = pipeline(
    "question-answering",
    model=model_name,
    tokenizer=model_name
)

contexto = """
O Brasil é um país da América do Sul.
Capital: Brasília
Moeda: Real
Receita de bolo simples: 2 xícaras de farinha, 3 ovos, 1 xícara de leite
"""


def responder(pergunta):
    # Versão adicionando o context
    try:
        resultado = qa_pipeline(
            question=pergunta,
            context=contexto # Necessary argument
        )
        return resultado['answer']
    except Exception as e:
        return f"Erro ao responder: {e}"

# Testes
print("1:", responder("Qual é a capital do Brasil?"))
print("2:", responder("Quantos ovos vai no bolo?"))
print("3:", responder("Qual é a moeda do Brasil?"))
print("4:", responder("Quanto é 2+2?"))