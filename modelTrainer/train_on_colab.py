from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, Dataset
from huggingface_hub import login
from dotenv import load_dotenv
import os

load_dotenv()
login(os.getenv('HUGGINGFACE_HUB_TOKEN'))

dataset = load_dataset("csv", data_files={"train": "./train.csv", "test": "./test.csv"})

#model_name = "adalbertojunior/distilbert-portuguese-cased"
model_name = "neuralmind/bert-base-portuguese-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)


def mapCol(batch):
  batch['label'] = [0 if l == 'produtivo' else 1 for l in batch['label']]
  return batch

def combineSubjectAndBody(batch):
  batch['text'] = [f"{sub.lower()} {body.lower()}" for sub, body in zip(batch['subject'], batch['body'])]
  return batch

def tokenize(batch):
  return tokenizer(batch['text'], padding=True, truncation=True)

dataset = dataset.map(mapCol, batched=True)
dataset = dataset.map(combineSubjectAndBody, batched=True)
dataset = dataset.map(tokenize, batched=True)

training_args = TrainingArguments(
  output_dir='./data/results',
  eval_strategy="epoch",
  learning_rate=5e-5,
  per_device_train_batch_size=8, #4 ou 8
  num_train_epochs=4,
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

trainer.train()
trainer.push_to_hub()
