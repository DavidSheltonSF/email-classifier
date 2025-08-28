from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from transformers import pipeline



model = AutoModelForSequenceClassification.from_pretrained('./data/model', id2label={0: 'produtivo', 1: 'improdutivo'})
tokenizer = AutoTokenizer.from_pretrained('./data/tokenizer')
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

text_produtivo = 'Relatório financeiro Favor revisar o relatório financeiro antes da reunião de diretoria.'
text_improdutivo = 'Agradeçemos pelo feedback Agradecemos seu retorno sobre a pesquisa de clima.'

result = classifier('Valeu pela resposta Obrigado por me responder. Eu estava realmente ansioso com isso')
print(result)