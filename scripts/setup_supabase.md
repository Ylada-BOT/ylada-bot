# 🚀 Configurar Supabase - BOT by YLADA

## 📋 Passo a Passo

### 1. Criar Projeto no Supabase

1. Acesse: https://supabase.com
2. Faça login ou crie uma conta
3. Clique em "New Project"
4. Preencha:
   - **Name**: ylada-bot (ou outro nome)
   - **Database Password**: Anote essa senha!
   - **Region**: Escolha a mais próxima (ex: South America)
5. Clique em "Create new project"
6. Aguarde a criação (pode levar alguns minutos)

### 2. Obter String de Conexão

1. No projeto do Supabase, vá em **Settings** > **Database**
2. Role até **Connection string** > **URI**
3. Copie a string (formato: `postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres`)
4. Substitua `[PASSWORD]` pela senha que você criou

### 3. Criar Tabelas

**Opção A: Via SQL Editor (Recomendado)**

1. No Supabase, vá em **SQL Editor**
2. Clique em **New query**
3. Abra o arquivo `scripts/create_tables_supabase.sql`
4. Cole todo o conteúdo no editor
5. Clique em **Run** (ou Ctrl+Enter)
6. Aguarde a execução
7. Verifique se todas as tabelas foram criadas (deve aparecer "Success")

**Opção B: Via Script Python**

1. Configure a variável de ambiente:
```bash
export DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres"
```

2. Execute o script:
```bash
python3 scripts/init_db.py
```

### 4. Configurar .env

Crie um arquivo `.env` na raiz do projeto:

```env
# Supabase
DATABASE_URL=postgresql://postgres:[SUA_SENHA]@db.[SEU_PROJETO].supabase.co:5432/postgres

# Segurança
SECRET_KEY=sua-chave-secreta-aqui
JWT_SECRET_KEY=sua-jwt-secret-key-aqui

# WhatsApp
WHATSAPP_SERVER_PORT=5001
WHATSAPP_WEBHOOK_URL=http://localhost:5002/webhook

# IA
AI_PROVIDER=openai
AI_API_KEY=sua-openai-api-key
AI_MODEL=gpt-4o-mini

# Aplicação
APP_URL=http://localhost:5002
DEBUG=true
```

### 5. Verificar Tabelas Criadas

No Supabase, vá em **Table Editor** e verifique se aparecem as tabelas:
- ✅ users
- ✅ plans
- ✅ tenants
- ✅ subscriptions
- ✅ instances
- ✅ flows
- ✅ conversations
- ✅ messages
- ✅ leads
- ✅ notifications

### 6. Testar Conexão

```bash
# Instalar dependências (se ainda não instalou)
pip install -r requirements.txt

# Testar conexão
python3 -c "from config.database import engine; print('Conexão OK!' if engine else 'Erro')"
```

---

## ✅ Pronto!

Agora você pode:
1. Rodar o servidor: `python3 web/app.py`
2. Acessar: http://localhost:5002
3. Criar uma conta em `/register`
4. Fazer login em `/login`

---

## 🔍 Troubleshooting

### Erro: "connection refused"
- Verifique se a DATABASE_URL está correta
- Verifique se o projeto Supabase está ativo
- Verifique se a senha está correta

### Erro: "relation does not exist"
- Execute o script SQL novamente
- Verifique se todas as tabelas foram criadas

### Erro: "permission denied"
- Verifique se está usando a senha correta
- Verifique se o projeto não foi pausado (projetos gratuitos podem pausar após inatividade)

---

## 📝 Notas

- **Projeto Gratuito**: Supabase oferece plano gratuito com 500MB de banco
- **Backup**: As tabelas são criadas automaticamente, mas faça backup regular
- **Segurança**: Nunca commite o arquivo `.env` no Git!

---

**Próximo passo**: Após criar as tabelas, execute `python3 scripts/init_db.py` para criar dados iniciais (planos e usuário admin).
