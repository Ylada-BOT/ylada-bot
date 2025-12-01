# 🔐 Como Preencher o Arquivo .env

## 📝 Instruções

1. **Abra o arquivo `.env`** na raiz do projeto
2. **Cole suas chaves** nas linhas correspondentes:

```env
# Supabase - Cole suas chaves aqui:
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_anon_key_aqui
SUPABASE_SERVICE_KEY=sua_service_key_aqui

# GitHub Token - Cole seu token aqui:
GITHUB_TOKEN=ghp_seu_token_aqui

# Secret Key - Gere uma chave aleatória:
SECRET_KEY=qualquer_chave_aleatoria_segura_aqui
```

## 🔑 Onde Encontrar as Chaves

### Supabase
1. Acesse: https://app.supabase.com
2. Selecione seu projeto
3. **Settings** → **API**
4. Copie:
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_KEY`
   - **service_role key** → `SUPABASE_SERVICE_KEY`

### GitHub Token
1. Acesse: https://github.com/settings/tokens
2. **Generate new token (classic)**
3. Marque: `repo`
4. Copie o token → `GITHUB_TOKEN`

## ⚠️ Importante

- ✅ O arquivo `.env` **NÃO será commitado** (está no .gitignore)
- ✅ Mantenha suas chaves seguras
- ✅ Não compartilhe o arquivo `.env`

