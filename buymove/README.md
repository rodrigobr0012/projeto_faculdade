# BuyMove

Protótipo de loja de carros online construído com FastAPI, MongoDB e um front-end simples em HTML, CSS e JavaScript.

## Estrutura do projeto

```
buymove/
├── backend/
│   ├── database/
│   │   ├── connection.py
│   │   └── seed.py
│   ├── main.py
│   ├── models/
│   │   └── car_model.py
│   └── routes/
│       └── car_routes.py
├── data/
│   └── cars.json
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
└── requirements.txt
```

## Pré-requisitos

- Python 3.11+
- MongoDB em execução (local ou remoto)

## Como executar o back-end

1. Instale as dependências a partir da pasta `buymove`:

   ```bash
   cd buymove
   pip install -r requirements.txt
   ```

2. Defina as variáveis de ambiente se necessário (por padrão o projeto usa `mongodb://localhost:27017` e o banco `buymove`).

3. Inicie a API:

   ```bash
   uvicorn backend.main:app --reload
   ```

   No primeiro carregamento os dados do arquivo `data/cars.json` serão inseridos no MongoDB caso a coleção esteja vazia.

## Como executar o front-end

Basta abrir o arquivo `frontend/index.html` em um navegador. A página utiliza `fetch` para consumir a API disponível em `http://localhost:8000`.

## Endpoints principais

- `GET /cars` – Lista todos os carros.
- `GET /cars/{id}` – Retorna os detalhes de um carro pelo ID.
- `GET /cars/search?query=...` – Busca carros por modelo ou marca.
- `POST /cars` – Cadastra um novo carro.

## Seeds

Os dados iniciais são carregados automaticamente no startup da aplicação a partir de `data/cars.json`. Para inserir manualmente execute:

```bash
cd buymove
python -m backend.database.seed
```

## Licença

Projeto desenvolvido para fins educacionais.
