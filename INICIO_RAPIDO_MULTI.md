# 🚀 Início Rápido - Multi-Instance (4 Telefones)

## ✅ O que foi criado:

1. ✅ **Sistema de Banco de Dados** (`src/database.py`)
   - Suporta SQLite (desenvolvimento) e PostgreSQL (produção)
   - Multi-tenancy completo
   - Isolamento de dados por conta

2. ✅ **Gerenciador de Instâncias** (`src/instance_manager.py`)
   - Gerencia múltiplas instâncias WhatsApp
   - Suporta 4+ telefones simultaneamente
   - Monitoramento automático

3. ✅ **Gerenciador de Contas** (`src/account_manager.py`)
   - Multi-tenancy completo
   - Isolamento de contatos, campanhas, conversas

4. ✅ **API Multi-Instance** (`web/app_multi.py`)
   - Endpoints para gerenciar 4 instâncias
   - API REST completa
   - Compatível com código existente

5. ✅ **Script de Inicialização** (`scripts/init_4_accounts.py`)
   - Configura suas 4 contas rapidamente

---

## 🎯 Como Usar AGORA:

### **Passo 1: Inicializar suas 4 contas**

```bash
cd "/Users/air/Ylada BOT"
python scripts/init_4_accounts.py
```

O script vai pedir:
- 4 números WhatsApp (formato: 5511999999999)
- Nome para cada conta

### **Passo 2: Iniciar servidor**

```bash
python web/app_multi.py
```

### **Passo 3: Conectar telefones**

1. Acesse: http://localhost:5002
2. Veja os 4 telefones listados
3. Para cada telefone:
   - Clique para ver QR Code
   - Escaneie com o WhatsApp correspondente
   - Aguarde conectar

### **Passo 4: Usar!**

- Envie mensagens via API
- Gerencie contatos (isolados por conta)
- Crie campanhas (isoladas por conta)
- Veja conversas (isoladas por conta)

---

## 📡 Exemplos de Uso:

### **Listar todas as instâncias:**
```bash
curl http://localhost:5002/api/instances
```

### **Ver QR Code de uma instância:**
```bash
curl http://localhost:5002/api/instances/<account_id>/qr
```

### **Enviar mensagem:**
```bash
curl -X POST http://localhost:5002/api/accounts/<account_id>/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5511999999999",
    "message": "Olá! Como posso ajudar?"
  }'
```

### **Listar contatos de uma conta:**
```bash
curl http://localhost:5002/api/accounts/<account_id>/contacts
```

---

## 🗄️ Banco de Dados:

### **SQLite (Padrão - Desenvolvimento)**
- Arquivo: `data/ylada_bot.db`
- Funciona imediatamente
- Perfeito para desenvolvimento

### **PostgreSQL (Produção)**
Para usar PostgreSQL/Supabase:

1. Configure variáveis de ambiente:
```bash
export DB_HOST=seu-host.supabase.co
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=sua-senha
```

2. Mude no `app_multi.py`:
```python
db = Database(use_sqlite=False)  # Usa PostgreSQL
```

---

## 🎯 Arquitetura:

```
┌─────────────────────────────────────┐
│      FRONTEND (Futuro)              │
│  - Dashboard multi-instância        │
│  - Gerenciar 4 telefones            │
└──────────────┬──────────────────────┘
               │
               │ REST API
               │
┌──────────────▼──────────────────────┐
│      BACKEND (app_multi.py)          │
│  - InstanceManager (4 instâncias)   │
│  - AccountManager (multi-tenancy)    │
└──────────────┬──────────────────────┘
               │
               │
┌──────────────▼──────────────────────┐
│      DATABASE (SQLite/PostgreSQL)    │
│  - accounts (4 contas)              │
│  - instances (4 instâncias)         │
│  - contacts (isolados)              │
│  - campaigns (isolados)             │
└─────────────────────────────────────┘
```

---

## ✅ Vantagens:

1. ✅ **Funciona AGORA** com 4 telefones
2. ✅ **Escala depois** para comercializar
3. ✅ **Não quebra código** existente (app.py ainda funciona)
4. ✅ **Isolamento garantido** (multi-tenancy)
5. ✅ **Fácil adicionar** novos telefones/contas
6. ✅ **Robusto** (banco de dados real)

---

## 📚 Documentação:

- `ARQUITETURA_SAAS_PRONTA.md` - Arquitetura completa
- `README_MULTI_INSTANCE.md` - Documentação da API
- `ARQUITETURA_RECOMENDADA.md` - Recomendações futuras

---

## 🚀 Próximos Passos:

1. ✅ Execute `scripts/init_4_accounts.py`
2. ✅ Inicie `web/app_multi.py`
3. ✅ Conecte seus 4 telefones
4. ✅ Teste enviando mensagens
5. ✅ Use normalmente!

**Tudo pronto para usar! 🎉**

