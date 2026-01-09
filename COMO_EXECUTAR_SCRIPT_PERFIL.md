# 📝 Como Executar o Script SQL de Perfil

## 🎯 O QUE O SCRIPT FAZ

O script `add_user_profile_fields.sql` adiciona dois novos campos na tabela `users`:
- **`phone`** - Para armazenar o telefone do usuário
- **`photo_url`** - Para armazenar a URL da foto de perfil

Esses campos são necessários para a funcionalidade de edição de perfil funcionar corretamente.

---

## ✅ PASSO A PASSO - EXECUTAR NO SUPABASE

### **1. Acesse o Supabase**

1. Abra seu navegador
2. Acesse: **https://supabase.com/dashboard**
3. Faça login na sua conta
4. Selecione o projeto do BOT by YLADA

---

### **2. Abra o SQL Editor**

1. No menu lateral esquerdo, procure por **"SQL Editor"**
2. Clique em **"SQL Editor"**
3. Você verá uma tela com um editor de código SQL

---

### **3. Criar Nova Query**

1. Clique no botão **"New query"** (ou "Nova consulta")
2. Uma nova aba será aberta no editor

---

### **4. Copiar o Script**

1. Abra o arquivo `scripts/add_user_profile_fields.sql` no seu projeto
2. Selecione **TODO o conteúdo** do arquivo (Ctrl+A ou Cmd+A)
3. Copie (Ctrl+C ou Cmd+C)

---

### **5. Colar no SQL Editor**

1. Volte para o Supabase (SQL Editor)
2. Cole o conteúdo no editor (Ctrl+V ou Cmd+V)
3. Você verá o script completo no editor

---

### **6. Executar o Script**

1. Clique no botão **"Run"** (ou pressione `Ctrl+Enter` / `Cmd+Enter`)
2. Aguarde alguns segundos
3. Você verá uma mensagem de sucesso na parte inferior

**O que você deve ver:**
- ✅ Mensagem: "Success. No rows returned"
- ✅ Ou mensagens de NOTICE indicando que as colunas foram adicionadas

---

### **7. Verificar se Funcionou**

1. No menu lateral, clique em **"Table Editor"**
2. Clique na tabela **"users"**
3. Role até ver as colunas
4. Você deve ver as novas colunas:
   - ✅ `phone`
   - ✅ `photo_url`

---

## 🖼️ VISUALIZAÇÃO DOS PASSOS

```
1. Supabase Dashboard
   └─> 2. SQL Editor (menu lateral)
       └─> 3. New query
           └─> 4. Colar script
               └─> 5. Run (Ctrl+Enter)
                   └─> 6. Verificar em Table Editor
```

---

## ⚠️ OBSERVAÇÕES IMPORTANTES

- ✅ O script é **seguro** - ele verifica se as colunas já existem antes de adicionar
- ✅ Você pode executar o script **várias vezes** sem problemas
- ✅ Não vai apagar ou modificar dados existentes
- ✅ Apenas **adiciona** as colunas se elas não existirem

---

## ❓ PROBLEMAS COMUNS

### **Erro: "permission denied"**
- Verifique se você está logado como administrador do projeto
- Verifique se o projeto está ativo (não pausado)

### **Erro: "relation users does not exist"**
- A tabela `users` ainda não foi criada
- Execute primeiro o script `create_tables_supabase_fix.sql`

### **Não vejo as colunas após executar**
- Aguarde alguns segundos e atualize a página
- Verifique se executou o script completo (todas as linhas)

---

## 🎉 PRONTO!

Após executar o script com sucesso:
1. ✅ As colunas `phone` e `photo_url` estarão disponíveis
2. ✅ A funcionalidade de editar perfil funcionará corretamente
3. ✅ Você poderá adicionar telefone e foto de perfil

---

**Última atualização:** 27/01/2025

