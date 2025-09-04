from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

text_produtivo = 'Relatório financeiro Favor revisar o relatório financeiro antes da reunião de diretoria.'
text_improdutivo = 'Agradeçemos pelo feedback Agradecemos seu retorno sobre a pesquisa de clima.'

model = "davidshelton/email-classifier-soft"
client = InferenceClient(token=os.getenv('HUGGINGFACE_HUB_TOKEN'))

result = client.text_classification(text_improdutivo, model=model)

print(result)