# 🧹 Limpar e Recriar Tabelas no Supabase

## ⚠️ ATENÇÃO

O erro que você recebeu indica que há **tabelas antigas com tipos diferentes** (UUID vs INTEGER).

## 🔍 Passo 1: Verificar o que existe

Antes de limpar, vamos ver o que já existe:

1. No Supabase, vá em **SQL Editor**
2. Abra o arquivo: `scripts/verificar_tabelas_existentes.sql`
3. Copie e execute
4. Isso vai mostrar:
   - Quais tabelas existem
   - Quais têm tipos errados (UUID)
   - Quais foreign keys existem

## 🧹 Passo 2: Limpar TUDO

**IMPORTANTE**: Isso vai **APAGAR TODOS OS DADOS**!

1. No Supabase, vá em **SQL Editor**
2. Abra o arquivo: `scripts/clean_and_create_tables.sql`
3. **Leia o script** para entender o que ele faz
4. **Copie TODO o conteúdo**
5. **Cole no SQL Editor**
6. **Execute** (Run)

Este script:
- ✅ Remove TODAS as tabelas antigas (DROP CASCADE)
- ✅ Remove sequências antigas
- ✅ Cria tudo do zero com tipos consistentes (INTEGER)
- ✅ Cria índices
- ✅ Insere dados iniciais (planos)

## ✅ Passo 3: Verificar

Após executar, você deve ver:

```
✅ Tabelas criadas: 10
```

E a lista de tabelas:
- conversations
- flows
- instances
- leads
- messages
- notifications
- plans
- subscriptions
- tenants
- users

## 🎯 O que foi corrigido

### Problema anterior:
- Algumas tabelas tinham `id` como UUID
- Outras tinham `id` como INTEGER
- Foreign keys não funcionavam (tipos incompatíveis)

### Solução:
- ✅ Todas as tabelas agora usam `INTEGER` para `id`
- ✅ Usa `GENERATED ALWAYS AS IDENTITY` (padrão PostgreSQL moderno)
- ✅ Todas as foreign keys são consistentes
- ✅ Limpeza completa antes de criar

## 📋 Ordem de Execução

1. **Primeiro**: Execute `verificar_tabelas_existentes.sql` (para ver o que existe)
2. **Depois**: Execute `clean_and_create_tables.sql` (para limpar e criar)
3. **Verificar**: Confira se todas as 10 tabelas foram criadas

## 🔧 Se ainda der erro

### Erro: "permission denied"
- Verifique se você tem permissão de DROP no banco
- No Supabase, você deve ter permissão como owner do projeto

### Erro: "table does not exist"
- Isso é normal se as tabelas já foram removidas
- Continue executando o script

### Erro: "constraint already exists"
- O script usa `IF NOT EXISTS` onde possível
- Se der erro, pode ser que alguma constraint já exista
- Execute o DROP CASCADE novamente

## ✅ Após criar com sucesso

1. **Configure .env**:
```env
DATABASE_URL=postgresql://postgres:[SENHA]@db.[PROJETO].supabase.co:5432/postgres
```

2. **Execute script Python** (para criar dados iniciais):
```bash
python3 scripts/init_db.py
```

3. **Inicie servidor**:
```bash
python3 web/app.py
```

4. **Acesse**: http://localhost:5002/register

---

## 🎉 Pronto!

Agora todas as tabelas estão criadas corretamente com tipos consistentes!

---

**Dica**: Salve este script (`clean_and_create_tables.sql`) - você pode precisar dele novamente se precisar recriar tudo do zero.
