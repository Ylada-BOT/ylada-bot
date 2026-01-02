# 💾 Sistema de Backup - BOT by YLADA

## 📋 Como Usar

### 🔄 Fazer Backup (ANTES de reiniciar)

```bash
python3 backup_data.py
```

Isso vai criar:
- 📁 Pasta `backups/backup_YYYYMMDD_HHMMSS/` com todos os arquivos
- 📦 Arquivo ZIP `backups/backup_YYYYMMDD_HHMMSS.zip` (mais fácil de mover)

### 🔄 Restaurar Backup (DEPOIS de reiniciar)

```bash
python3 restore_data.py backups/backup_20241201_120000.zip
```

Ou se preferir usar a pasta:

```bash
python3 restore_data.py backups/backup_20241201_120000
```

## 📦 O que é salvo no backup?

✅ **Instâncias do usuário** (`data/user_instances.json`)
- Todas as instâncias WhatsApp criadas
- Portas configuradas
- Status das conexões

✅ **Sessões do WhatsApp** (`data/sessions/`)
- Sessões ativas do WhatsApp
- Permite reconectar sem escanear QR Code novamente

✅ **Organizações** (`data/organizations.json`)
- Se ainda existir no sistema

✅ **Fluxos** (`data/flows.json`)
- Se existir arquivo de fluxos

✅ **Configurações**
- `.env` (variáveis de ambiente)
- `config.json` (se existir)
- `web/config.py` (configurações do web)

## 🚀 Passo a Passo Completo

### 1. ANTES de reiniciar:

```bash
# Faz backup de tudo
python3 backup_data.py
```

### 2. Copie o arquivo ZIP para lugar seguro:
- Pendrive
- Google Drive
- Outro computador
- Email para você mesmo

### 3. DEPOIS de reiniciar:

```bash
# Restaura tudo
python3 restore_data.py backups/backup_YYYYMMDD_HHMMSS.zip
```

### 4. Inicie o servidor normalmente:

```bash
python3 web/app.py
```

## ⚠️ Importante

- **Sempre faça backup antes de reiniciar!**
- O backup inclui as sessões do WhatsApp, então você não precisa escanear QR Code novamente
- Guarde o arquivo ZIP em lugar seguro
- Você pode ter múltiplos backups (cada um com timestamp diferente)

## 📍 Localização dos Backups

Todos os backups ficam na pasta `backups/` na raiz do projeto:

```
Ylada BOT/
├── backups/
│   ├── backup_20241201_120000/
│   ├── backup_20241201_120000.zip
│   ├── backup_20241202_150000/
│   └── backup_20241202_150000.zip
├── data/
├── backup_data.py
└── restore_data.py
```

## 🔍 Verificar Backup

Para ver o que tem no backup:

```bash
# Se for ZIP
unzip -l backups/backup_YYYYMMDD_HHMMSS.zip

# Se for pasta
ls -la backups/backup_YYYYMMDD_HHMMSS/
```


