# Deploy no Vercel

O projeto já está configurado para rodar no Vercel (`vercel.json`, `api/index.py`, `requirements.txt` na raiz). Siga os passos abaixo.

## 1. Conectar o repositório

1. Acesse [vercel.com](https://vercel.com) e faça login (GitHub/GitLab/Bitbucket).
2. **Add New** → **Project**.
3. Importe o repositório do frigorifico-app.
4. **Root Directory:** deixe em branco.
5. **Framework Preset:** None.
6. Não altere **Build Command** nem **Output Directory**.
7. Avance e configure as variáveis antes do primeiro deploy.

## 2. Variáveis de ambiente

Em **Settings** → **Environment Variables** do projeto, crie:

| Nome | Valor |
|------|--------|
| `DATABASE_URL` | Connection string do Supabase (ex.: `postgresql://postgres:SENHA@db.xxx.supabase.co:5432/postgres`). Se a senha tiver `@` ou `,`, use URL-encode: `@` → `%40`, `,` → `%2C`. |
| `SECRET_KEY` | Chave secreta do Django. Gere uma com: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |

Opcionais:

- `DEBUG` = `0` ou `false` (produção).
- `ALLOWED_HOSTS` = `.vercel.app,.now.sh` (o padrão no código já inclui).

Marque para **Production** (e Preview/Development se quiser) e salve.

## 3. Deploy

1. Faça **Deploy** (ou **Redeploy**).
2. Use o link `https://seu-projeto.vercel.app` quando terminar.

## 4. Superusuário (login no app e admin)

As tabelas já estão no Supabase. Para criar um usuário de login:

**Local (com mesmo `DATABASE_URL` do Supabase):**

```powershell
cd venv
$env:DATABASE_URL='sua-connection-string-aqui'
.\Scripts\python.exe manage.py createsuperuser
```

Ou use um `.env` na raiz com `DATABASE_URL` e rode `.\Scripts\python.exe manage.py createsuperuser` com o venv ativado.

## 5. Se der erro

| Sintoma | Verificar |
|--------|-----------|
| 404 NOT_FOUND | `api/index.py` na raiz; **Root Directory** vazio em Settings. |
| 500 / ModuleNotFoundError | Pasta `venv/frigorifico_app` versionada (não ignorada no .gitignore). |
| 400 Bad Request | Variável `ALLOWED_HOSTS` com `.vercel.app,.now.sh`. |
| Erro de banco | `DATABASE_URL` em Production; senha URL-encoded se tiver `@` ou `,`. |
| Admin sem CSS | WhiteNoise já está em uso; confira logs em `/static/`. |

Logs: Vercel → projeto → último deploy → **Building** / **Functions**.
