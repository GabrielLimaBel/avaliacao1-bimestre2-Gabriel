# Base - Controle De Leituras

Esta é a aplicação-base da avaliação de reposição da turma 2V.

Ela já possui CRUD de leituras com SQLite, Blueprint de autenticação, Blueprint de leituras e uma função de segurança iniciada em `seguranca.py`. A autenticação com `session` e o controle de acesso por usuário ainda precisam ser implementados.

## Executar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000`.

## Arquivos Principais

- `app.py`: cria a aplicação e registra os Blueprints.
- `auth.py`: rotas de cadastro, login e logout a serem completadas.
- `leituras.py`: rotas do CRUD de leituras.
- `seguranca.py`: função de proteção das rotas privadas.
- `database.py`: funções de banco de dados.
- `templates/`: páginas HTML.

## Observação

Não substitua a aplicação por outro projeto. A tarefa é adaptar esta base para autenticação com `session`, vinculando cada leitura ao usuário logado.

## Respostas

1. Por que as rotas de leituras ficaram em leituras.py e não em app.py?

   - para separar as rotas de leitura em um Blueprint, e também para organizar melhor o codigo


2. Como a aplicação identifica o usuário logado usando session?

   - A aplicação armazena o "usuario_id" na sessão quando o usuário faz login.


3. Como seguranca.py, leituras.py e database.py impedem acesso de leituras de outro usuário?

   - antes de permite o acesso as rotas de leituras, a função "exigir_login" em "seguranca.py" analisa se o usuario ta logado. E também o baco de dados filtra pelo id, pra que cada usuario vejo somente a sua propria leitura
