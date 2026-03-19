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

## 6. Deploy automático com GitHub Actions

Foi criado o workflow:

- `.github/workflows/deploy-prod.yml`

Fluxo:

1. Em push na `main`, roda `python manage.py migrate` no banco do Supabase.
2. Se migração passar, dispara deploy no Vercel via Deploy Hook.

### Secrets necessários no GitHub

No repositório GitHub: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret | Valor |
|--------|-------|
| `SUPABASE_DATABASE_URL` | URL de conexão do Supabase (pooler, ex.: porta 6543) |
| `DJANGO_SECRET_KEY` | mesma `SECRET_KEY` usada em produção |
| `VERCEL_DEPLOY_HOOK_URL` | URL do Deploy Hook do Vercel |

### Como criar o Deploy Hook no Vercel

1. Vercel → projeto → **Settings** → **Git**.
2. Em **Deploy Hooks**, crie um hook para branch `main`.
3. Copie a URL gerada e salve em `VERCEL_DEPLOY_HOOK_URL` no GitHub.

Observação: a URL de banco do GitHub (`SUPABASE_DATABASE_URL`) deve apontar para o mesmo banco usado no Vercel para manter schema e app sincronizados.
