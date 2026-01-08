# 💾 Guia Completo: Backup e Restauração

## 🎯 OBJETIVO

Este guia explica como fazer backup de **TUDO** antes de reiniciar o computador, para não perder nenhuma informação.

---

## 📋 O QUE É SALVO NO BACKUP

✅ **Banco de Dados** - Todos os dados (usuários, organizações, robôs, fluxos, conversas, leads)  
✅ **Sessões WhatsApp** - Conexões dos robôs (QR codes, autenticações)  
✅ **Configurações** - Arquivo .env, configurações de IA, etc.  
✅ **Fluxos** - Automações criadas  
✅ **Logs** - Histórico do sistema  

---

## 🚀 COMO FAZER BACKUP

### **Método 1: Script Automático (Recomendado)**

```bash
# 1. Dar permissão de execução
chmod +x scripts/backup_completo.sh

# 2. Executar backup
./scripts/backup_completo.sh
```

**O que acontece:**
- ✅ Cria um arquivo `backup_YYYYMMDD_HHMMSS.zip` (ou .tar.gz)
- ✅ Salva TUDO necessário
- ✅ Compacta tudo em um único arquivo

### **Método 2: Manual (Se o script não funcionar)**

```bash
# 1. Criar diretório de backup
mkdir -p backup_manual

# 2. Backup do banco de dados
pg_dump $DATABASE_URL > backup_manual/database_backup.sql

# 3. Backup das sessões WhatsApp
cp -r data/sessions backup_manual/

# 4. Backup das configurações
cp .env backup_manual/
cp data/ai_config.json backup_manual/ 2>/dev/null || true

# 5. Compactar
zip -r backup_manual.zip backup_manual
```

---

## 🔄 COMO RESTAURAR APÓS REINICIAR

### **Método 1: Script Automático (Recomendado)**

```bash
# 1. Dar permissão de execução
chmod +x scripts/restore_backup.sh

# 2. Restaurar backup
./scripts/restore_backup.sh backup_20241223_120000.zip
```

### **Método 2: Manual**

```bash
# 1. Extrair backup
unzip backup_20241223_120000.zip
# ou
tar -xzf backup_20241223_120000.tar.gz

# 2. Restaurar banco de dados
psql $DATABASE_URL < backup_*/database_backup.sql

# 3. Restaurar sessões WhatsApp
cp -r backup_*/sessions/* data/sessions/

# 4. Restaurar configurações
cp backup_*/.env .env
cp backup_*/ai_config.json data/ 2>/dev/null || true
```

---

## ⚠️ IMPORTANTE: SESSÕES WHATSAPP

**Atenção:** As sessões WhatsApp podem expirar após reiniciar o computador.

**O que fazer:**
1. ✅ Faça backup das sessões (já está incluído)
2. ⚠️ Após restaurar, verifique cada robô
3. 🔄 Se algum robô desconectar, escaneie o QR code novamente

**Dica:** Se possível, mantenha o computador ligado ou use um servidor na nuvem.

---

## 📦 ONDE GUARDAR O BACKUP

**Opções seguras:**
- ✅ Google Drive
- ✅ Dropbox
- ✅ OneDrive
- ✅ Pendrive/USB
- ✅ Servidor na nuvem
- ✅ Email para você mesmo

**⚠️ NUNCA compartilhe o arquivo `.env`** - ele contém senhas!

---

## 🔍 VERIFICAR SE O BACKUP ESTÁ COMPLETO

Após fazer backup, verifique se contém:

```
backup_YYYYMMDD_HHMMSS/
├── database_backup.sql    ✅ Backup do banco
├── sessions/              ✅ Sessões WhatsApp
├── .env                   ✅ Configurações
├── ai_config.json         ✅ Configuração de IA
├── flows.json             ✅ Fluxos (se houver)
└── INFO_BACKUP.txt        ✅ Informações do backup
```

---

## 🚨 EM CASO DE PROBLEMAS

### **Problema: Script não executa**

```bash
# Dar permissão
chmod +x scripts/backup_completo.sh
chmod +x scripts/restore_backup.sh
```

### **Problema: pg_dump não encontrado**

```bash
# macOS
brew install postgresql

# Linux
sudo apt-get install postgresql-client
```

### **Problema: Banco de dados não restaura**

1. Verifique se o PostgreSQL está rodando
2. Verifique se DATABASE_URL está correta
3. Tente restaurar manualmente:
   ```bash
   psql $DATABASE_URL < database_backup.sql
   ```

---

## 📝 CHECKLIST ANTES DE REINICIAR

- [ ] ✅ Backup completo executado
- [ ] ✅ Arquivo de backup salvo em local seguro
- [ ] ✅ Anotado onde está o backup
- [ ] ✅ Verificado que o backup contém tudo necessário

---

## 🎯 RESUMO RÁPIDO

**Fazer Backup:**
```bash
./scripts/backup_completo.sh
```

**Restaurar Backup:**
```bash
./scripts/restore_backup.sh backup_20241223_120000.zip
```

**Pronto!** Seus dados estão seguros! 🎉

---

**Última atualização:** 2024-12-23










