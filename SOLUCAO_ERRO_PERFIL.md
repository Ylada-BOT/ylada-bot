# 🔧 SOLUÇÃO: Erro ao Salvar Perfil

## 🐛 Problema

Ao tentar salvar alterações no perfil, aparece o erro:
```
column users.phone does not exist
```

Isso acontece porque as colunas `phone` e `photo_url` não existem na tabela `users` do banco de dados.

---

## ✅ Solução: Executar Script SQL

### Passo 1: Acessar Supabase

1. Acesse: https://supabase.com
2. Faça login no seu projeto
3. No menu lateral, clique em **"SQL Editor"** (ícone `</>`)
4. Clique em **"New query"**

### Passo 2: Copiar e Executar Script

1. Abra o arquivo: `scripts/add_user_profile_fields.sql`
2. **Copie TODO o conteúdo** (Ctrl+A / Cmd+A, depois Ctrl+C / Cmd+C)
3. **Cole no SQL Editor** do Supabase
4. Clique em **"Run"** (ou pressione Ctrl+Enter / Cmd+Enter)

### Passo 3: Verificar

O script deve mostrar:
- ✅ "Coluna phone adicionada com sucesso"
- ✅ "Coluna photo_url adicionada com sucesso"
- Uma lista com todas as colunas da tabela `users`

---

## 🎯 O que o Script Faz

O script adiciona duas colunas na tabela `users`:

1. **`phone`** (VARCHAR(20)) - Para armazenar o telefone do usuário
2. **`photo_url`** (VARCHAR(500)) - Para armazenar a URL da foto de perfil

O script é seguro: ele verifica se as colunas já existem antes de adicionar, então não causa erro se executar novamente.

---

## ✅ Após Executar o Script

1. **Recarregue a página** do perfil (F5)
2. **Tente salvar** as alterações novamente
3. **Deve funcionar!** ✅

---

## 📋 Script Completo

Se você não encontrar o arquivo, aqui está o script:

```sql
-- Adiciona coluna phone (telefone) se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'users' 
        AND column_name = 'phone'
    ) THEN
        ALTER TABLE public.users ADD COLUMN phone VARCHAR(20);
        RAISE NOTICE 'Coluna phone adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna phone já existe';
    END IF;
END $$;

-- Adiciona coluna photo_url (URL da foto de perfil) se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'users' 
        AND column_name = 'photo_url'
    ) THEN
        ALTER TABLE public.users ADD COLUMN photo_url VARCHAR(500);
        RAISE NOTICE 'Coluna photo_url adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna photo_url já existe';
    END IF;
END $$;
```

---

## 💡 Melhorias Implementadas

Agora, quando houver erro de coluna não encontrada, a mensagem será mais clara:
- ✅ Explica qual é o problema
- ✅ Diz qual script executar
- ✅ Fornece instruções passo a passo

---

**Última atualização:** 2025-01-27

