# desafio-autoU Classificador de Email

## Como testar

1 - Clonar o repositório
```bash
git clone https://github.com/DavidSheltonSF/desafio-autoU.git
```

2 - Configure um arquivo .env com as seguintes variáveis
```bash
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=5501
```

3 - No arquivo main.py, modifique a linha abaixo, chamando o método load_from_hub_and_save(), dessa
forma o modelo de IA será baixado do hub e salvo localmente

```python
classifier = ClassifierModel()
classifier.load_model_localy() # <- substitua esse método
```

4 - Rode o comando para construir o container
```bash
docker compose up --build
```

## Observações

Como o modelo necessário para rodar a aplicação é muito pesado, a hospedagem na nuvem não foi possível.