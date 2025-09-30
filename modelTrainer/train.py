from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
from huggingface_hub import login
from dotenv import load_dotenv
import os
import torch
import torch.nn.utils.prune as prune
import evaluate
import numpy as np

load_dotenv()
login(os.getenv('HUGGINGFACE_HUB_TOKEN'))

dataset = load_dataset("csv", data_files={"train": "./backend/modelTrainer/train.csv", "test": "./backend/modelTrainer/test.csv"})

model_name = "adalbertojunior/distilbert-portuguese-cased"
#model_name = "neuralmind/bert-base-portuguese-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2,
    dtype=torch.bfloat16
)


# Preprocess
def preprocess(batch):
  batch['label'] = [0 if l == 'produtivo' else 1 for l in batch['label']]
  batch['text'] = [f"{sub.lower()} {body.lower()}" for sub, body in zip(batch['subject'], batch['body'])]
  return tokenizer(batch['text'], padding="max_length", max_length=24, truncation=True)

dataset['train'] = dataset['train'].map(preprocess, batched=True)
dataset['test'] = dataset['test'].map(preprocess, batched=True)
print(dataset['train'])
print(dataset['test'])

# carregar métricas
accuracy = evaluate.load("accuracy")
precision = evaluate.load("precision")
recall = evaluate.load("recall")
f1 = evaluate.load("f1")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy.compute(predictions=predictions, references=labels),
        "precision": precision.compute(predictions=predictions, references=labels, average="weighted"),
        "recall": recall.compute(predictions=predictions, references=labels, average="weighted"),
        "f1": f1.compute(predictions=predictions, references=labels, average="weighted"),
    }

#trainer.push_to_hub()
model.save_pretrained("./backend/model", safe_serialization=True)
tokenizer.save_pretrained("./backend/model", safe_serialization=True)
# Coloca modelo em eval
#model.eval()
training_args = TrainingArguments(
  output_dir='./data/results',
  eval_strategy="epoch",
  save_strategy="epoch",
  save_total_limit=1,
  learning_rate=5e-5,
  per_device_train_batch_size=16, #4 ou 8 quando executar localmente
  num_train_epochs=6,
  weight_decay=0.03,
  push_to_hub=True,
  hub_model_id="davidshelton/email-classifier-soft",
  report_to="none"
)

trainer = Trainer(
  model=model,
  args=training_args,
  train_dataset=dataset['train'],
  eval_dataset=dataset['test'],
)

print('training')
trainer.train()
print('trained')

print('Applying pruning')
# Aplica pruning em todas as camadas lineares
for name, module in model.named_modules():
    if isinstance(module, torch.nn.Linear):
        prune.l1_unstructured(module, name="weight", amount=0.3)

print('pruniung applied!')

for name, module in model.named_modules():
    if isinstance(module, torch.nn.Linear):
        prune.remove(module, name="weight")

model.to(torch.bfloat16)

model.push_to_hub("davidshelton/email-classifier-soft")
tokenizer.push_to_hub("davidshelton/email-classifier-soft")

print('Model Uploaded!!!')
