# 📦 Como Criar o Repositório no GitHub

## ⚠️ Importante

**Não consigo criar o repositório automaticamente** - você precisa criar manualmente no GitHub.

## 🚀 Passo a Passo

### 1. Criar Repositório

1. Acesse: **https://github.com/new**
2. **Repository name**: `ylada-bot`
3. **Description** (opcional): `WhatsApp Bot com automação e gestão de contatos`
4. **Visibility**: ✅ **Public**
5. **IMPORTANTE**: ❌ **NÃO marque**:
   - Add README
   - Add .gitignore
   - Add license
6. Clique em **"Create repository"**

### 2. Depois de Criar

Execute no terminal:

```bash
cd "/Users/air/Ylada BOT"
git push -u origin main
```

Quando pedir:
- **Username**: Seu usuário GitHub
- **Password**: Cole o **GITHUB_TOKEN** (do arquivo .env)

## 🔐 Alternativa: Usar Token na URL

Se preferir, configure o token diretamente:

```bash
# Pegue o token do arquivo .env
GITHUB_TOKEN=$(grep GITHUB_TOKEN .env | cut -d '=' -f2)

# Configure o remote com o token
git remote set-url origin https://${GITHUB_TOKEN}@github.com/Ylada-BOT/ylada-bot.git

# Faça push
git push -u origin main
```

## ✅ Verificação

Após o push, acesse:
**https://github.com/Ylada-BOT/ylada-bot**

Você deve ver todos os arquivos do projeto!

