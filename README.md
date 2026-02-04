# 🌌 Star Wars API — Case Técnico Backend Python (PowerOfData)

API RESTful construída em **Python + FastAPI**, consumindo dados da **SWAPI (https://swapi.dev/)** e expondo endpoints filtráveis para consulta de informações de Star Wars.

---

## 🚀 Como Executar

### Opção 1: Docker Compose (Recomendado)

```bash
# Iniciar API + MongoDB
make docker-up

# Ou manualmente
docker compose up -d

# Ver logs
make docker-logs

# Parar containers
make docker-down
```

A API estará disponível em: http://localhost:8000

### Opção 2: Execução Local

```bash
# 1. Instalar dependências
make dev
# ou: pip install -e ".[dev]"

# 2. Iniciar MongoDB (necessário)
docker run -d -p 27017:27017 --name mongo mongo:7.0

# 3. Executar a API
make run
# ou: uvicorn app.main:app --reload
```

### Comandos Disponíveis (Makefile)

| Comando | Descrição |
|---------|-----------|
| `make help` | Lista todos os comandos |
| `make dev` | Instala dependências de desenvolvimento |
| `make run` | Inicia a API localmente |
| `make test` | Executa os testes |
| `make docker-up` | Inicia com Docker Compose |
| `make docker-down` | Para os containers |
| `make docker-logs` | Visualiza logs |
| `make lint` | Executa linter (ruff) |
| `make format` | Formata código (black) |

---

## 📖 Documentação Interativa

Após iniciar a API, acesse:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## ✅ Requisitos do Case (atendidos)

- **Python** como linguagem principal
- Consumo de dados via **SWAPI**
- Endpoints para consulta de **filmes, personagens, planetas, espécies, naves e veículos**
- Suporte a **filtros via query params**
- Desenho preparado para deploy em **GCP** (Cloud Functions + API Gateway/Apigee)

---

## 🧱 Stack

| Tecnologia | Uso |
|------------|-----|
| Python 3.11+ | Linguagem principal |
| FastAPI | Framework web |
| Pydantic | Validação de dados |
| HTTPX | Cliente HTTP assíncrono |
| Motor | Driver MongoDB assíncrono |
| python-jose | JWT tokens |
| passlib/bcrypt | Hash de senhas |
| Pytest | Testes unitários |

---

## 🔌 API — Documentação de Rotas

### 🔐 Autenticação

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/api/v1/auth/token` | Login (retorna access + refresh tokens) | ❌ |
| `POST` | `/api/v1/auth/refresh` | Renovar tokens usando refresh token | ❌ |

**Exemplo de Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -d "username=seu_usuario&password=sua_senha"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "abc123...",
  "token_type": "bearer"
}
```

---

### 👤 Usuários

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/api/v1/users` | Criar novo usuário | ❌ |
| `GET` | `/api/v1/users` | Listar todos os usuários | ✅ |
| `GET` | `/api/v1/users/me` | Obter usuário atual | ✅ |
| `GET` | `/api/v1/users/{id}` | Obter usuário por ID | ✅ |
| `PATCH` | `/api/v1/users/{id}` | Atualizar usuário | ✅ |
| `DELETE` | `/api/v1/users/{id}` | Deletar usuário | ✅ |

**Exemplo de Criação de Usuário:**
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{"username": "luke", "email": "luke@jedi.com", "password": "force123"}'
```

---

### 🎬 Filmes

| Método | Endpoint | Descrição | Filtros |
|--------|----------|-----------|---------|
| `GET` | `/api/v1/films` | Listar todos os filmes | `search`, `page` |
| `GET` | `/api/v1/films/{id}` | Obter filme por ID | - |

**Exemplo:**
```bash
# Listar filmes
curl "http://localhost:8000/api/v1/films"

# Buscar por título
curl "http://localhost:8000/api/v1/films?search=hope"

# Obter filme específico
curl "http://localhost:8000/api/v1/films/1"
```

**Campos retornados:** `id`, `title`, `episode_id`, `opening_crawl`, `director`, `producer`, `release_date`, `characters`, `planets`, `starships`, `vehicles`, `species`

---

### 👥 Personagens (People)

| Método | Endpoint | Descrição | Filtros |
|--------|----------|-----------|---------|
| `GET` | `/api/v1/people` | Listar todos os personagens | `search`, `page` |
| `GET` | `/api/v1/people/{id}` | Obter personagem por ID | - |

**Exemplo:**
```bash
# Buscar por nome
curl "http://localhost:8000/api/v1/people?search=luke"
```

**Campos retornados:** `id`, `name`, `height`, `mass`, `hair_color`, `skin_color`, `eye_color`, `birth_year`, `gender`, `homeworld`, `films`, `species`, `vehicles`, `starships`

---

### 🌍 Planetas

| Método | Endpoint | Descrição | Filtros |
|--------|----------|-----------|---------|
| `GET` | `/api/v1/planets` | Listar todos os planetas | `search`, `page` |
| `GET` | `/api/v1/planets/{id}` | Obter planeta por ID | - |

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/planets?search=tatooine"
```

**Campos retornados:** `id`, `name`, `rotation_period`, `orbital_period`, `diameter`, `climate`, `gravity`, `terrain`, `surface_water`, `population`, `residents`, `films`

---

### 👽 Espécies

| Método | Endpoint | Descrição | Filtros |
|--------|----------|-----------|---------|
| `GET` | `/api/v1/species` | Listar todas as espécies | `search`, `page` |
| `GET` | `/api/v1/species/{id}` | Obter espécie por ID | - |

**Campos retornados:** `id`, `name`, `classification`, `designation`, `average_height`, `skin_colors`, `hair_colors`, `eye_colors`, `average_lifespan`, `homeworld`, `language`, `people`, `films`

---

### 🚀 Naves Estelares (Starships)

| Método | Endpoint | Descrição | Filtros |
|--------|----------|-----------|---------|
| `GET` | `/api/v1/starships` | Listar todas as naves | `search`, `page` |
| `GET` | `/api/v1/starships/{id}` | Obter nave por ID | - |

**Campos retornados:** `id`, `name`, `model`, `manufacturer`, `cost_in_credits`, `length`, `max_atmosphering_speed`, `crew`, `passengers`, `cargo_capacity`, `consumables`, `hyperdrive_rating`, `MGLT`, `starship_class`, `pilots`, `films`

---

### 🚗 Veículos

| Método | Endpoint | Descrição | Filtros |
|--------|----------|-----------|---------|
| `GET` | `/api/v1/vehicles` | Listar todos os veículos | `search`, `page` |
| `GET` | `/api/v1/vehicles/{id}` | Obter veículo por ID | - |

**Campos retornados:** `id`, `name`, `model`, `manufacturer`, `cost_in_credits`, `length`, `max_atmosphering_speed`, `crew`, `passengers`, `cargo_capacity`, `consumables`, `vehicle_class`, `pilots`, `films`

---

## ⚙️ Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `MONGODB_URL` | `mongodb://localhost:27017` | URL de conexão MongoDB |
| `MONGODB_DB_NAME` | `starwars_db` | Nome do banco de dados |
| `JWT_SECRET_KEY` | - | Chave secreta para JWT (obrigatório em produção) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Tempo de expiração do access token |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Tempo de expiração do refresh token |

Você pode criar um arquivo `.env` na raiz do projeto:
```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=starwars_db
JWT_SECRET_KEY=sua-chave-super-secreta
```

---

## 🗂️ Arquitetura do Projeto

<details>
<summary><strong>📐 Arquitetura e organização de pastas</strong></summary>

```text
app/
├── api/
│   ├── routers/
│   │   ├── auth.py          # POST /auth/token, /auth/refresh
│   │   ├── films.py         # GET /films, /films/{id}
│   │   ├── people.py        # GET /people, /people/{id}
│   │   ├── planets.py       # GET /planets, /planets/{id}
│   │   ├── species.py       # GET /species, /species/{id}
│   │   ├── starships.py     # GET /starships, /starships/{id}
│   │   ├── vehicles.py      # GET /vehicles, /vehicles/{id}
│   │   └── user.py          # CRUD /users
│   ├── controllers/
│   └── dependencies.py      # Auth guards (get_current_user, etc.)
├── application/
│   ├── usecases/            # Casos de uso por recurso
│   └── service/
│       └── auth_service.py  # JWT & password hashing
├── domain/
│   ├── entities/            # Entidades de domínio
│   ├── repositories/        # Interfaces de repositório
│   └── errors.py
├── infrastructure/
│   ├── db/
│   │   └── database.py      # MongoDB connection (Motor)
│   ├── clients/
│   │   └── swapi_client.py  # HTTPX async client
│   └── repositories/        # Implementações MongoDB
├── schemas/                 # Pydantic models
├── core/
│   └── config.py            # Settings (pydantic-settings)
└── main.py
test/
├── conftest.py              # Fixtures & mocks
└── usecases/                # Testes por caso de uso
```

</details>

---

## 🧭 Diagramas (SVG)

<details>
<summary><strong>Rotas — Filmes (lista)</strong></summary>

![Rotas — Filmes (lista)](docs/diagrams/Diagrama%20de%20rotas%20Films.svg)

</details>

<details>
<summary><strong>Rotas — Filmes (por id)</strong></summary>

![Rotas — Filmes (por id)](docs/diagrams/Diagrama%20de%20rotas%20film%20id.svg)

</details>

<details>
<summary><strong>Rotas — Personagens (lista)</strong></summary>

![Rotas — Personagens (lista)](docs/diagrams/Diagrama%20de%20rotas%20people.svg)

</details>

<details>
<summary><strong>Rotas — Personagens (por id)</strong></summary>

![Rotas — Personagens (por id)](docs/diagrams/Diagrama%20de%20rotas%20people%20id.svg)

</details>

<details>
<summary><strong>Rotas — Planetas (lista)</strong></summary>

![Rotas — Planetas (lista)](docs/diagrams/Diagrama%20de%20rotas%20planets.svg)

</details>

<details>
<summary><strong>Rotas — Planetas (por id)</strong></summary>

![Rotas — Planetas (por id)](docs/diagrams/Diagrama%20de%20rotas%20planets%20id.svg)

</details>

<details>
<summary><strong>Rotas — Espécies (lista)</strong></summary>

![Rotas — Espécies (lista)](docs/diagrams/Diagrama%20de%20rotas%20species.svg)

</details>

<details>
<summary><strong>Rotas — Espécies (por id)</strong></summary>

![Rotas — Espécies (por id)](docs/diagrams/Diagrama%20de%20rotas%20species%20id.svg)

</details>

<details>
<summary><strong>Rotas — Starships (lista)</strong></summary>

![Rotas — Starships (lista)](docs/diagrams/Diagrama%20de%20rotas%20starships.svg)

</details>

<details>
<summary><strong>Rotas — Starships (por id)</strong></summary>

![Rotas — Starships (por id)](docs/diagrams/Diagrama%20de%20rotas%20starships%20id.svg)

</details>

<details>
<summary><strong>Rotas — Veículos (lista)</strong></summary>

![Rotas — Veículos (lista)](docs/diagrams/Diagrama%20de%20rotas%20vehicles.svg)

</details>

<details>
<summary><strong>Rotas — Veículos (por id)</strong></summary>

![Rotas — Veículos (por id)](docs/diagrams/Diagrama%20de%20rotas%20vehicles%20id.svg)

</details>

---

## 🧪 Testes

```bash
# Rodar todos os testes
make test

# Ou manualmente
pytest test/ -v
```

- **36 testes** cobrindo todos os casos de uso
- Repositórios fake/in-memory para isolamento
- Mocks para SWAPI e MongoDB

---

## 👨‍💻 Autor

Isaque Elis da Silva
