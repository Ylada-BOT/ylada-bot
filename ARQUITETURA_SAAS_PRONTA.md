# 🏗️ Arquitetura SaaS Pronta - 4 Telefones + Comercialização

## 🎯 Objetivo
- ✅ Funcionar AGORA com 4 telefones seus
- ✅ Comercializar depois sem quebrar código
- ✅ Arquitetura robusta e escalável
- ✅ Não quebrar o que já funciona

---

## 📐 Arquitetura Proposta

### **Estrutura Híbrida (Evolutiva)**

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  - Dashboard multi-instância                            │
│  - Gerenciar 4 telefones                                │
│  - Interface para clientes (futuro)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ REST API
                     │
┌────────────────────▼────────────────────────────────────┐
│              BACKEND API (Flask)                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Instance Manager (Gerencia 4 instâncias)        │ │
│  │  - WhatsAppWebJSHandler por instância            │ │
│  │  - Portas diferentes (5001, 5002, 5003, 5004)   │ │
│  │  - Sessões isoladas                               │ │
│  └──────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Account Manager (Multi-tenancy)                │ │
│  │  - Cada telefone = 1 account (agora)            │ │
│  │  - Depois: 1 account = vários telefones          │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
                     │
┌────────────────────▼────────────────────────────────────┐
│         BANCO DE DADOS (PostgreSQL/Supabase)            │
│  - accounts (suas 4 contas)                            │
│  - instances (4 instâncias WhatsApp)                  │
│  - contacts (isolados por account)                    │
│  - campaigns (isolados por account)                   │
│  - conversations (isolados por account)                │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Schema do Banco de Dados

### **1. Tabela: accounts (Suas 4 contas)**
```sql
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,  -- Número do WhatsApp
    plan VARCHAR(50) DEFAULT 'owner',   -- owner, free, basic, pro
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Inserir suas 4 contas
INSERT INTO accounts (name, phone) VALUES
    ('Conta 1', '5511999999999'),
    ('Conta 2', '5511888888888'),
    ('Conta 3', '5511777777777'),
    ('Conta 4', '5511666666666');
```

### **2. Tabela: instances (Instâncias WhatsApp)**
```sql
CREATE TABLE instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    instance_name VARCHAR(100) NOT NULL,  -- Ex: "numero1"
    port INTEGER UNIQUE NOT NULL,        -- 5001, 5002, 5003, 5004
    status VARCHAR(50) DEFAULT 'disconnected', -- disconnected, connecting, connected
    qr_code TEXT,
    last_connected TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(account_id, instance_name)
);

-- Inserir 4 instâncias (uma por conta)
INSERT INTO instances (account_id, instance_name, port) 
SELECT id, 'instance_' || phone, 
    CASE 
        WHEN phone = '5511999999999' THEN 5001
        WHEN phone = '5511888888888' THEN 5002
        WHEN phone = '5511777777777' THEN 5003
        WHEN phone = '5511666666666' THEN 5004
    END
FROM accounts;
```

### **3. Tabela: contacts (Isolado por account)**
```sql
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    name VARCHAR(255),
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(account_id, phone)  -- Mesmo telefone pode existir em contas diferentes
);

CREATE INDEX idx_contacts_account ON contacts(account_id);
```

### **4. Tabela: conversations (Isolado por account)**
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    contact_id UUID REFERENCES contacts(id),
    message TEXT NOT NULL,
    from_me BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_account ON conversations(account_id);
CREATE INDEX idx_conversations_contact ON conversations(contact_id);
```

### **5. Tabela: campaigns (Isolado por account)**
```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    message TEXT,
    qr_code_url TEXT,
    link TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_campaigns_account ON campaigns(account_id);
```

---

## 🔧 Implementação

### **1. Instance Manager (Gerencia 4 instâncias)**

```python
# src/instance_manager.py
from typing import Dict, List, Optional
from whatsapp_webjs_handler import WhatsAppWebJSHandler
import uuid

class InstanceManager:
    """Gerencia múltiplas instâncias WhatsApp"""
    
    def __init__(self, db):
        self.db = db
        self.instances: Dict[str, WhatsAppWebJSHandler] = {}
        self._load_instances()
    
    def _load_instances(self):
        """Carrega instâncias do banco"""
        instances_data = self.db.get_all_instances()
        for inst_data in instances_data:
            handler = WhatsAppWebJSHandler(
                instance_name=inst_data['instance_name'],
                port=inst_data['port']
            )
            self.instances[inst_data['id']] = {
                'handler': handler,
                'data': inst_data
            }
    
    def get_instance(self, account_id: str) -> Optional[WhatsAppWebJSHandler]:
        """Retorna handler da instância da conta"""
        instance_data = self.db.get_instance_by_account(account_id)
        if instance_data:
            instance_id = instance_data['id']
            return self.instances[instance_id]['handler']
        return None
    
    def start_instance(self, account_id: str) -> bool:
        """Inicia instância da conta"""
        handler = self.get_instance(account_id)
        if handler:
            return handler.start_server()
        return False
    
    def get_all_instances_status(self) -> List[Dict]:
        """Retorna status de todas as instâncias"""
        status_list = []
        for instance_id, instance_info in self.instances.items():
            handler = instance_info['handler']
            status_list.append({
                'id': instance_id,
                'account_id': instance_info['data']['account_id'],
                'instance_name': instance_info['data']['instance_name'],
                'port': instance_info['data']['port'],
                'status': 'connected' if handler.is_ready() else 'disconnected',
                'qr_code': handler.get_qr_code() if not handler.is_ready() else None
            })
        return status_list
```

### **2. Account Manager (Multi-tenancy)**

```python
# src/account_manager.py
from typing import Dict, Optional
import uuid

class AccountManager:
    """Gerencia contas (multi-tenancy)"""
    
    def __init__(self, db):
        self.db = db
    
    def get_account(self, account_id: str) -> Optional[Dict]:
        """Retorna dados da conta"""
        return self.db.get_account(account_id)
    
    def get_account_by_phone(self, phone: str) -> Optional[Dict]:
        """Retorna conta pelo telefone"""
        return self.db.get_account_by_phone(phone)
    
    def create_account(self, name: str, phone: str) -> Dict:
        """Cria nova conta"""
        account = {
            'id': str(uuid.uuid4()),
            'name': name,
            'phone': phone,
            'plan': 'owner',
            'status': 'active'
        }
        self.db.create_account(account)
        return account
    
    def get_account_contacts(self, account_id: str):
        """Retorna contatos da conta (isolado)"""
        return self.db.get_contacts_by_account(account_id)
    
    def get_account_campaigns(self, account_id: str):
        """Retorna campanhas da conta (isolado)"""
        return self.db.get_campaigns_by_account(account_id)
```

### **3. Database Layer (Abstração)**

```python
# src/database.py
import psycopg2
from typing import Dict, List, Optional
import os

class Database:
    """Camada de abstração do banco de dados"""
    
    def __init__(self):
        self.conn = self._connect()
    
    def _connect(self):
        """Conecta ao PostgreSQL/Supabase"""
        return psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    
    def get_all_instances(self) -> List[Dict]:
        """Retorna todas as instâncias"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM instances")
            return [dict(row) for row in cur.fetchall()]
    
    def get_instance_by_account(self, account_id: str) -> Optional[Dict]:
        """Retorna instância da conta"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM instances WHERE account_id = %s",
                (account_id,)
            )
            row = cur.fetchone()
            return dict(row) if row else None
    
    def get_account(self, account_id: str) -> Optional[Dict]:
        """Retorna conta"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def get_contacts_by_account(self, account_id: str) -> List[Dict]:
        """Retorna contatos da conta (isolado)"""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM contacts WHERE account_id = %s",
                (account_id,)
            )
            return [dict(row) for row in cur.fetchall()]
    
    # ... outros métodos
```

### **4. API Refatorada (app.py)**

```python
# web/app.py (versão refatorada)
from flask import Flask, request, jsonify
from instance_manager import InstanceManager
from account_manager import AccountManager
from database import Database

app = Flask(__name__)

# Inicializa
db = Database()
account_manager = AccountManager(db)
instance_manager = InstanceManager(db)

@app.route('/api/instances', methods=['GET'])
def list_instances():
    """Lista todas as instâncias (seus 4 telefones)"""
    instances = instance_manager.get_all_instances_status()
    return jsonify({'instances': instances})

@app.route('/api/instances/<account_id>/start', methods=['POST'])
def start_instance(account_id: str):
    """Inicia instância de uma conta"""
    success = instance_manager.start_instance(account_id)
    return jsonify({'success': success})

@app.route('/api/instances/<account_id>/qr', methods=['GET'])
def get_instance_qr(account_id: str):
    """Retorna QR Code da instância"""
    handler = instance_manager.get_instance(account_id)
    if handler:
        qr = handler.get_qr_code()
        return jsonify({'qr': qr, 'ready': handler.is_ready()})
    return jsonify({'error': 'Instância não encontrada'}), 404

@app.route('/api/accounts/<account_id>/contacts', methods=['GET'])
def get_account_contacts(account_id: str):
    """Retorna contatos da conta (isolado)"""
    contacts = account_manager.get_account_contacts(account_id)
    return jsonify({'contacts': contacts})

@app.route('/api/accounts/<account_id>/send', methods=['POST'])
def send_message(account_id: str):
    """Envia mensagem via instância da conta"""
    data = request.get_json()
    handler = instance_manager.get_instance(account_id)
    
    if not handler:
        return jsonify({'error': 'Instância não encontrada'}), 404
    
    if not handler.is_ready():
        return jsonify({'error': 'WhatsApp não conectado'}), 400
    
    success = handler.send_message(
        data['phone'],
        data['message']
    )
    return jsonify({'success': success})
```

---

## 🚀 Como Funciona

### **AGORA (4 Telefones):**
1. Você cria 4 contas no banco (uma por telefone)
2. Cada conta tem 1 instância WhatsApp (porta diferente)
3. Interface mostra os 4 telefones
4. Cada telefone tem seus próprios contatos/campanhas (isolado)

### **DEPOIS (Comercialização):**
1. Cliente se registra → cria nova conta
2. Cliente conecta WhatsApp → cria instância
3. Dados ficam isolados automaticamente
4. Você pode ver todas as contas (admin)
5. Cliente vê só a dele

---

## 📋 Ordem de Implementação

### **FASE 1: Banco de Dados (1 dia)**
- ✅ Criar schema no Supabase
- ✅ Inserir suas 4 contas
- ✅ Criar 4 instâncias

### **FASE 2: Backend (2-3 dias)**
- ✅ Criar Database layer
- ✅ Criar InstanceManager
- ✅ Criar AccountManager
- ✅ Refatorar app.py

### **FASE 3: Frontend (2-3 dias)**
- ✅ Interface para gerenciar 4 instâncias
- ✅ Dashboard com status de cada uma
- ✅ QR Codes individuais
- ✅ Contatos isolados por instância

### **FASE 4: Testes (1 dia)**
- ✅ Testar com 4 telefones
- ✅ Validar isolamento
- ✅ Ajustar bugs

---

## ✅ Vantagens

1. **Funciona AGORA** com 4 telefones
2. **Escala depois** para comercializar
3. **Não quebra código** existente
4. **Isolamento garantido** (multi-tenancy)
5. **Fácil adicionar** novos telefones/contas
6. **Robusto** (banco de dados real)

---

## 🎯 Próximos Passos

Quer que eu comece implementando?
1. ✅ Schema do banco
2. ✅ InstanceManager
3. ✅ AccountManager
4. ✅ Refatorar app.py
5. ✅ Interface frontend

