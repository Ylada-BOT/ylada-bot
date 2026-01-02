# 📖 O que é TENANT?

## 🎯 Explicação Simples

**Tenant = Cliente**

Pense assim:
- **Você** (dono da plataforma) tem vários **clientes**
- Cada **cliente** = 1 **Tenant**
- Cada **Tenant** pode ter vários **Bots** (instâncias)

### Exemplo Prático:

```
Você (Plataforma YLADA)
│
├── Cliente 1: "Empresa ABC" (Tenant 1)
│   ├── Bot Vendas (Instância 1)
│   └── Bot Suporte (Instância 2)
│
├── Cliente 2: "Loja XYZ" (Tenant 2)
│   └── Bot Principal (Instância 3)
│
└── Cliente 3: "Distribuidora 123" (Tenant 3)
    ├── Bot Atacado (Instância 4)
    └── Bot Varejo (Instância 5)
```

---

## 💡 Por que usar Tenants?

### **Isolamento Total:**
- Cada cliente vê **só os seus bots**
- Dados isolados (conversas, leads, fluxos)
- Segurança (um cliente não vê dados de outro)

### **Multi-tenant:**
- Você pode ter **múltiplos clientes** na mesma plataforma
- Cada cliente paga sua assinatura
- Você gerencia tudo de um lugar

---

## 🔄 Fluxo de Uso

1. **Você cria um Tenant** (cliente)
   - Exemplo: "Empresa ABC"

2. **O cliente cria Bots** (instâncias)
   - Bot Vendas
   - Bot Suporte

3. **Cada Bot conecta um WhatsApp**
   - Bot Vendas → WhatsApp 1
   - Bot Suporte → WhatsApp 2

4. **Cada Bot tem seus próprios fluxos**
   - Bot Vendas → Fluxo de vendas
   - Bot Suporte → Fluxo de atendimento

---

## ⚠️ PROBLEMA ATUAL

O sistema está configurado para **multi-tenant** (vários clientes), mas você pode querer usar de forma **mais simples**:

### **Opção 1: Modo Simples (1 Tenant)**
- Você tem apenas 1 cliente (você mesmo)
- Cria 1 tenant
- Cria quantos bots quiser

### **Opção 2: Modo Multi-tenant (Vários Clientes)**
- Você tem vários clientes
- Cada cliente é um tenant
- Cada cliente cria seus bots

---

## 🛠️ CORREÇÃO

Vou simplificar para funcionar **sem banco de dados** no modo desenvolvimento:

1. **Criar tenant sem precisar de usuário no banco**
2. **Funcionar mesmo sem banco configurado**
3. **QR Code funcionar corretamente**

---

**Última atualização:** 13/12/2024





