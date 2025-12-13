# 📊 Como Criar as Tabelas no Supabase

## 🚀 Método Rápido (Recomendado)

### 1. Acesse o Supabase SQL Editor

1. Vá para: https://supabase.com
2. Faça login no seu projeto
3. No menu lateral, clique em **SQL Editor**
4. Clique em **New query**

### 2. Execute o Script SQL

1. Abra o arquivo: `scripts/create_tables_supabase.sql`
2. **Copie TODO o conteúdo** do arquivo
3. **Cole no SQL Editor** do Supabase
4. Clique em **Run** (ou pressione Ctrl+Enter / Cmd+Enter)
5. Aguarde alguns segundos
6. Deve aparecer: **Success. No rows returned**

### 3. Verificar Tabelas Criadas

1. No menu lateral, clique em **Table Editor**
2. Você deve ver todas as tabelas:
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

---

## 🔧 Método Alternativo (Script Python)

### 1. Configurar Conexão

Crie arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://postgres:[SUA_SENHA]@db.[SEU_PROJETO].supabase.co:5432/postgres
```

**Como obter a URL:**
1. No Supabase: Settings > Database
2. Role até "Connection string" > "URI"
3. Copie e substitua `[PASSWORD]` pela sua senha

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar Script

```bash
python3 scripts/init_db.py
```

O script vai:
- ✅ Criar todas as tabelas
- ✅ Criar planos padrão (Grátis, Básico, Pro, Enterprise)
- ✅ Criar usuário admin (admin@ylada.com / admin123)

---

## ✅ Verificação

Após criar as tabelas, teste a conexão:

```bash
python3 -c "from config.database import engine; print('✅ Conexão OK!' if engine else '❌ Erro')"
```

---

## 🎯 Próximo Passo

Depois de criar as tabelas:

1. **Configure o .env** com DATABASE_URL
2. **Inicie o servidor**: `python3 web/app.py`
3. **Acesse**: http://localhost:5002/register
4. **Crie sua conta** ou use: admin@ylada.com / admin123

---

## ❓ Problemas?

### Erro: "relation already exists"
- As tabelas já existem, tudo OK!

### Erro: "permission denied"
- Verifique se a senha está correta
- Verifique se o projeto Supabase está ativo

### Erro: "connection refused"
- Verifique se a DATABASE_URL está correta
- Verifique se o projeto não foi pausado

---

**Pronto!** Agora você tem todas as tabelas criadas e pode começar a usar o sistema! 🎉
