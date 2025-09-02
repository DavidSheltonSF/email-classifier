from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

# model = AutoModelForSequenceClassification.from_pretrained('./backend/model', id2label={0: 'produtivo', 1: 'improdutivo'})
# tokenizer = AutoTokenizer.from_pretrained('./backend/model')

# model = AutoModelForSequenceClassification.from_pretrained('davidshelton/email-classifier-soft', id2label={0: 'produtivo', 1: 'improdutivo'})
# tokenizer = AutoTokenizer.from_pretrained('davidshelton/email-classifier-soft')


classifier = pipeline('text-classification', model="davidshelton/email-classifier-soft-test", tokenizer="davidshelton/email-classifier-soft-test")

text_produtivo = 'Relatório financeiro Favor revisar o relatório financeiro antes da reunião de diretoria.'
text_improdutivo = 'Agradeçemos pelo feedback Agradecemos seu retorno sobre a pesquisa de clima.'

result = classifier('Valeu pela resposta Obrigado por me responder. Eu estava realmente ansioso com isso')
print(result)