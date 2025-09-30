from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

spam = 'URGENT! You have won a 1 week FREE membership in our £100,000 Prize Jackpot! Txt the word: CLAIM to No: 81010 T&C www.dbuk.net LCCLTD POBOX 4403LDNW1A7RW18'
ham = 'Eh u remember how 2 spell his name... Yes i did. He v naughty make until i v wet'

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend', 'model'))
print(model_path)
classifier = pipeline("text-classification", model=model_path, tokenizer=model_path)

result = classifier(ham)

print(result)