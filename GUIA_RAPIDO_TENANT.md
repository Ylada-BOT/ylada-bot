# 📖 Guia Rápido: O que é TENANT?

## 🎯 Explicação Simples

**Tenant = Cliente**

Imagine que você tem uma plataforma SaaS (como ManyChat):
- **Você** = Dono da plataforma
- **Tenant** = Cada cliente que usa sua plataforma
- **Instância/Bot** = Cada WhatsApp conectado

### Exemplo Real:

```
Você (Plataforma YLADA)
│
├── Cliente 1: "Empresa ABC" ← Este é um TENANT
│   ├── Bot Vendas (WhatsApp 1)
│   └── Bot Suporte (WhatsApp 2)
│
└── Cliente 2: "Loja XYZ" ← Este é outro TENANT
    └── Bot Principal (WhatsApp 3)
```

---

## ⚠️ PROBLEMA: Você não precisa de Tenants agora!

Se você está **testando** ou **usando sozinho**, pode pular os tenants e usar direto!

### **Solução Rápida:**

1. **Acesse o dashboard direto:**
   ```
   http://localhost:5002/
   ```

2. **Use o sistema simples:**
   - Clique em "Conectar WhatsApp"
   - Escaneie o QR Code
   - Pronto! Funciona sem tenants

3. **Quando quiser vender para clientes:**
   - Aí sim configure o banco de dados
   - Aí sim use o sistema de tenants

---

## 🔧 CORREÇÃO DOS ERROS

### **Erro ao Criar Tenant:**

**Causa:** Banco de dados não configurado

**Solução:**
- **Opção 1:** Use `/dashboard` direto (sem tenants)
- **Opção 2:** Configure banco de dados primeiro

### **QR Code Não Funciona:**

**Causa:** Servidor Node.js não está rodando

**Solução:**
```bash
# Inicie o servidor WhatsApp
node whatsapp_server.js

# Ou use o sistema antigo
# Acesse /qr diretamente
```

---

## 💡 RECOMENDAÇÃO

**Por enquanto, use assim:**

1. Acesse: `http://localhost:5002/`
2. Clique em "Conectar WhatsApp"
3. Use `/qr` para escanear
4. Funciona sem precisar criar tenants!

**Depois, quando quiser vender:**
- Configure PostgreSQL
- Use sistema de tenants
- Cada cliente terá seus próprios bots

---

**Última atualização:** 13/12/2024





