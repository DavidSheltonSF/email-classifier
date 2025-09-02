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

3 - Rode o comando para construir o container
```bash
docker compose up --build
```

A primeira vez que a aplicação rodar, será feito o download do modelo de inteligência artificial
treinado que está hospedado em davidshelton/email-classifier-soft


## Observações

Como o modelo necessário para rodar a aplicação é muito pesado, não foi a hospedagem na nuvem não foi possível.