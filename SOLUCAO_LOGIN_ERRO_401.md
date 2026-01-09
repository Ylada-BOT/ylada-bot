# 🔧 Solução: Erro 401 "Credenciais Inválidas" no Login

## ⚠️ PROBLEMA

Você está vendo o erro **"Credenciais inválidas"** (401) ao tentar fazer login porque:

1. ❌ O banco de dados não está conectando (senha incorreta)
2. ✅ O usuário existe no arquivo `data/users.json`
3. ⚠️ O sistema tenta usar o banco primeiro, e quando falha, pode não fazer fallback corretamente

---

## ✅ SOLUÇÃO RÁPIDA (2 OPÇÕES)

### **OPÇÃO 1: Corrigir a Senha do Banco (Recomendado)**

1. **No Supabase:**
   - Vá em **Settings** → **Database**
   - Role até **"Database password"**
   - Clique em **"Reset database password"**
   - **Copie a nova senha**

2. **No arquivo `.env.local`:**
   - Abra o arquivo
   - Encontre: `DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:...`
   - Substitua a senha pela nova que você copiou
   - Salve o arquivo

3. **Reinicie o servidor:**
   ```bash
   # Pare o servidor (Ctrl+C)
   # Inicie novamente
   python3 web/app.py
   ```

4. **Teste o login novamente**

---

### **OPÇÃO 2: Usar Modo Simplificado (Temporário)**

Se não conseguir corrigir a senha agora, você pode forçar o sistema a usar apenas o arquivo JSON:

1. **No arquivo `.env.local`:**
   - Adicione ou modifique:
   ```bash
   # Força modo simplificado (sem banco)
   USE_SIMPLE_AUTH_ONLY=true
   ```

2. **Reinicie o servidor**

3. **Teste o login**

---

## 🔍 VERIFICAR SE O USUÁRIO EXISTE

O usuário `portalmagra@gmail.com` existe no arquivo JSON. Verifique se a senha está correta.

**Para resetar a senha do usuário no JSON:**

1. Execute o script:
```bash
python3 scripts/reset_user_password.py portalmagra@gmail.com
```

Ou edite manualmente o arquivo `data/users.json` (não recomendado, pois precisa gerar o hash da senha).

---

## 📝 CHECKLIST

- [ ] Senha do banco resetada no Supabase
- [ ] `.env.local` atualizado com a nova senha
- [ ] Servidor reiniciado
- [ ] Login testado

---

## 🎯 PRÓXIMOS PASSOS

Após corrigir a conexão com o banco:
1. ✅ O login funcionará normalmente
2. ✅ Os dados serão sincronizados do JSON para o banco
3. ✅ Tudo funcionará corretamente

---

**Última atualização:** 27/01/2025

