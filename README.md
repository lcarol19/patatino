# 🐾 PATATINO — Plataforma de Adoção Responsável

Portal web desenvolvido para a ONG **Cafofe — Casa dos Focinhos Felizes**
como Projeto Integrador II do curso de Computação.

## Grupo 23 — PI II

## Tecnologias

| Requisito PI | Tecnologia |
|---|---|
| Framework web | Python + Flask |
| Banco de dados | MySQL (Aiven) |
| JavaScript | Máscaras CPF/RG, busca CEP, preview de fotos |
| Nuvem | Aiven (banco) + Cloudinary (fotos) + Render (hospedagem) |
| API externa | ViaCEP — preenchimento automático de endereço |
| Acessibilidade | Bootstrap 5 + ARIA + WCAG 2.1 AA |
| Controle de versão | Git + GitHub |
| Testes | pytest |
| PDF | WeasyPrint — Termo de Responsabilidade |

## Arquitetura

```
Padrão: Repository + Service + Controller (OO)

models/          → entidades de domínio (dataclasses)
repositories/    → acesso ao banco (todo SQL aqui)
services/        → regras de negócio
controllers/     → rotas Flask (Blueprints)
templates/       → HTML Jinja2
static/          → CSS, JS, imagens
tests/           → pytest
```

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/patatino.git
cd patatino/flask_src

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp ../.env.example .env
# Edite o .env com suas credenciais

# 5. Coloque o ca.pem do Aiven em flask_src/

# 6. Crie o banco
# Execute banco/patatino.sql no MySQL

# 7. Rode o servidor
python app.py
```

Acesse: http://localhost:5000

## Rodando os testes

```bash
cd flask_src
pytest tests/ -v
```

## Deploy no Render

1. Suba o código no GitHub
2. Acesse [render.com](https://render.com) → New → Blueprint
3. Conecte o repositório
4. Preencha as variáveis de ambiente no painel
5. Render faz o deploy automaticamente

## Rotas

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Catálogo de animais |
| GET | `/animal/<id>` | Detalhe do animal |
| GET/POST | `/cadastrar` | Cadastrar animal |
| GET/POST | `/editar/<id>` | Editar animal |
| POST | `/excluir/<id>` | Excluir animal |
| GET/POST | `/adotar/<id>` | Formulário de adoção |
| GET | `/adocao/confirmacao/<id>` | Confirmação |
| GET | `/termo/<id>` | Download do PDF |
| GET | `/api/cep/<cep>` | Proxy ViaCEP |

## ONG Cafofe

- 🌐 [cafofe.org](https://www.cafofe.org)
- 📸 [@cafofe.oficial](https://www.instagram.com/cafofe.oficial/)
- 📧 contato@cafofe.org
