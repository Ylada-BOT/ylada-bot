# 🔑 Como Regenerar Token do GitHub

## 📋 PASSO A PASSO

### **1. Acesse as Configurações do GitHub**

1. Faça login no GitHub
2. Clique na sua foto de perfil (canto superior direito)
3. Clique em **Settings** (Configurações)

---

### **2. Vá para Developer Settings**

1. No menu lateral esquerdo, role até o final
2. Clique em **Developer settings**

---

### **3. Acesse Personal Access Tokens**

1. No menu lateral, clique em **Personal access tokens**
2. Escolha **Tokens (classic)** ou **Fine-grained tokens**

**Recomendação:** Use **Tokens (classic)** para mais compatibilidade

---

### **4. Revogue o Token Antigo (Importante!)**

1. Encontre o token antigo na lista
2. Clique nos **3 pontinhos** ao lado
3. Clique em **Revoke** (Revogar)
4. Confirme a revogação

**⚠️ IMPORTANTE:** Isso invalida o token antigo imediatamente!

---

### **5. Crie um Novo Token**

1. Clique em **Generate new token**
2. Escolha **Generate new token (classic)**

---

### **6. Configure o Novo Token**

**Nome do token:**
```
Ylada BOT - Local Development
```

**Expiração:**
- Escolha uma data (ex: 90 dias) ou **No expiration** (sem expiração)

**Permissões (scopes):**
Marque as seguintes permissões:
- ✅ **repo** (Full control of private repositories)
  - Isso inclui: repo:status, repo_deployment, public_repo, repo:invite, security_events
- ✅ **workflow** (Update GitHub Action workflows) - se usar Actions

**Outras permissões opcionais:**
- Se precisar de mais permissões, marque conforme necessário

---

### **7. Gere e Copie o Token**

1. Role até o final da página
2. Clique em **Generate token**
3. **COPIE O TOKEN IMEDIATAMENTE!**
   - ⚠️ Você só verá o token UMA VEZ!
   - Se fechar a página, terá que criar outro

---

### **8. Atualize no Seu Projeto**

#### **Opção A: Atualizar Remote URL (Recomendado)**

```bash
# Remove remote antigo
git remote remove origin

# Adiciona novo remote com token novo
git remote add origin https://ghp_SEU_TOKEN_NOVO_AQUI@github.com/Ylada-BOT/ylada-bot.git

# Verifica
git remote -v
```

#### **Opção B: Usar Git Credential Helper**

```bash
# Salva credenciais
git config --global credential.helper store

# Na próxima vez que fizer push, digite:
# Username: seu-usuario-github
# Password: ghp_SEU_TOKEN_NOVO_AQUI
```

#### **Opção C: Usar SSH (Mais Seguro)**

1. Gere uma chave SSH:
```bash
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"
```

2. Adicione a chave pública ao GitHub:
   - Settings > SSH and GPG keys > New SSH key
   - Cole o conteúdo de `~/.ssh/id_ed25519.pub`

3. Mude o remote para SSH:
```bash
git remote set-url origin git@github.com:Ylada-BOT/ylada-bot.git
```

---

## 🔒 SEGURANÇA

### **Boas Práticas:**

1. ✅ **Nunca commite tokens no código**
2. ✅ **Use variáveis de ambiente** para tokens
3. ✅ **Revogue tokens antigos** quando não usar mais
4. ✅ **Use tokens com expiração** quando possível
5. ✅ **Dê permissões mínimas necessárias**

### **Se o Token Vazar:**

1. Revogue imediatamente no GitHub
2. Gere um novo token
3. Atualize todos os lugares onde usa o token
4. Se estava no histórico do Git, remova (já fizemos isso!)

---

## 📝 EXEMPLO DE USO

### **Atualizar Remote com Novo Token:**

```bash
# Ver token atual (oculto por segurança)
git remote -v

# Atualizar com novo token
git remote set-url origin https://ghp_NOVO_TOKEN_AQUI@github.com/Ylada-BOT/ylada-bot.git

# Testar
git push origin main
```

---

## 🆘 TROUBLESHOOTING

### **Erro: "Authentication failed"**

- Verifique se o token está correto
- Verifique se o token não expirou
- Verifique se tem as permissões corretas (repo)

### **Erro: "Permission denied"**

- Verifique se o token tem permissão `repo`
- Verifique se você tem acesso ao repositório

### **Token não funciona após criar**

- Aguarde alguns segundos (pode levar um momento para ativar)
- Verifique se copiou o token completo
- Tente criar um novo token

---

**Última atualização:** 23/12/2024

