# 📤 Como Fazer Push para GitHub

## ⚡ Método Rápido (Script Automático)

### 1️⃣ Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. **Nome**: `ylada-bot`
3. **Visibilidade**: Public
4. **IMPORTANTE**: NÃO marque nenhuma opção:
   - ❌ Add README
   - ❌ Add .gitignore  
   - ❌ Add license
5. Clique em **"Create repository"**

### 2️⃣ Executar Script

```bash
./push_to_github.sh
```

O script vai:
- ✅ Verificar se tem commits
- ✅ Perguntar seu usuário GitHub
- ✅ Conectar ao repositório
- ✅ Fazer push automaticamente

## 🔧 Método Manual

Se preferir fazer manualmente:

```bash
# 1. Adicionar remote (substitua YladaLead pelo seu usuário)
git remote add origin https://github.com/YladaLead/ylada-bot.git

# 2. Renomear branch para main (se necessário)
git branch -M main

# 3. Fazer push
git push -u origin main
```

## ❓ Problemas Comuns

### "Repository not found"
- **Causa**: Repositório não existe no GitHub
- **Solução**: Crie o repositório primeiro (passo 1)

### "Permission denied"
- **Causa**: Usuário/URL incorreto
- **Solução**: Verifique o nome do usuário/organização

### "Authentication failed"
- **Causa**: Precisa autenticar
- **Solução**: Use token de acesso pessoal ou SSH

## 🔐 Autenticação

Se pedir senha, você precisa usar um **Personal Access Token**:

1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token
3. Marque: `repo`
4. Use o token como senha

