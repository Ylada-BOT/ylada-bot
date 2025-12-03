# 🚀 Ylada BOT - Multi-Instance Setup

## 📋 Configuração Rápida (4 Telefones)

### 1. Inicializar Contas

Execute o script de inicialização:

```bash
python scripts/init_4_accounts.py
```

O script vai pedir:
- 4 números WhatsApp (formato: 5511999999999)
- Nome para cada conta (opcional)

Isso vai criar:
- 4 contas no banco de dados
- 4 instâncias WhatsApp (portas 5001, 5002, 5003, 5004)

### 2. Iniciar Servidor

```bash
python web/app_multi.py
```

### 3. Conectar Telefones

1. Acesse: http://localhost:5002
2. Veja os 4 telefones listados
3. Clique em cada um para ver o QR Code
4. Escaneie com o WhatsApp correspondente

---

## 📡 API Endpoints

### Instâncias

```bash
# Listar todas as instâncias
GET /api/instances

# Status de uma instância
GET /api/instances/<account_id>/status

# QR Code de uma instância
GET /api/instances/<account_id>/qr

# Iniciar instância
POST /api/instances/<account_id>/start

# Parar instância
POST /api/instances/<account_id>/stop
```

### Contas

```bash
# Listar contas
GET /api/accounts

# Dados de uma conta
GET /api/accounts/<account_id>
```

### Contatos (Isolado por conta)

```bash
# Listar contatos da conta
GET /api/accounts/<account_id>/contacts

# Criar contato
POST /api/accounts/<account_id>/contacts
{
  "phone": "5511999999999",
  "name": "João Silva",
  "tags": ["cliente", "vip"]
}
```

### Campanhas (Isolado por conta)

```bash
# Listar campanhas da conta
GET /api/accounts/<account_id>/campaigns

# Criar campanha
POST /api/accounts/<account_id>/campaigns
{
  "name": "Promoção Black Friday",
  "message": "Olá! Confira nossa promoção!"
}
```

### Mensagens

```bash
# Enviar mensagem
POST /api/accounts/<account_id>/send
{
  "phone": "5511999999999",
  "message": "Olá! Como posso ajudar?"
}

# Listar chats
GET /api/accounts/<account_id>/chats

# Mensagens de um chat
GET /api/accounts/<account_id>/chats/<chat_id>/messages
```

---

## 🗄️ Banco de Dados

### SQLite (Desenvolvimento - Padrão)

O sistema usa SQLite por padrão. Os dados ficam em:
```
data/ylada_bot.db
```

### PostgreSQL (Produção)

Para usar PostgreSQL/Supabase:

1. Configure variáveis de ambiente:
```bash
export DB_HOST=seu-host.supabase.co
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=sua-senha
export DB_PORT=5432
```

2. Mude no `app_multi.py`:
```python
db = Database(use_sqlite=False)  # Usa PostgreSQL
```

---

## 🎯 Como Funciona

### AGORA (4 Telefones):
- Cada telefone = 1 conta
- Cada conta = 1 instância WhatsApp
- Dados isolados por conta
- Interface mostra os 4 telefones

### DEPOIS (Comercialização):
- Cliente se registra → cria conta
- Cliente conecta WhatsApp → cria instância
- Dados isolados automaticamente
- Você vê todas as contas (admin)
- Cliente vê só a dele

---

## 🔧 Estrutura

```
src/
├── database.py          # Camada de banco de dados
├── instance_manager.py  # Gerencia múltiplas instâncias
└── account_manager.py   # Gerencia contas (multi-tenancy)

web/
└── app_multi.py         # API Flask multi-instância

scripts/
└── init_4_accounts.py  # Script de inicialização
```

---

## ✅ Vantagens

1. ✅ **Funciona AGORA** com 4 telefones
2. ✅ **Escala depois** para comercializar
3. ✅ **Não quebra código** existente
4. ✅ **Isolamento garantido** (multi-tenancy)
5. ✅ **Fácil adicionar** novos telefones/contas
6. ✅ **Robusto** (banco de dados real)

---

## 🐛 Troubleshooting

### Instância não inicia
- Verifique se a porta está livre
- Verifique se Node.js está instalado
- Veja os logs no terminal

### QR Code não aparece
- Aguarde alguns segundos após iniciar
- Tente reiniciar a instância
- Verifique se o servidor Node.js está rodando

### Erro de banco de dados
- Verifique se o diretório `data/` existe
- Execute o script de inicialização novamente
- Verifique permissões de escrita

---

## 📞 Próximos Passos

1. ✅ Configure suas 4 contas
2. ✅ Conecte os telefones
3. ✅ Teste envio de mensagens
4. ✅ Crie campanhas
5. ✅ Use normalmente!

