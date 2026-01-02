# 🎯 PASSO A PASSO: Configurar Sua Conta como DONO

**Objetivo:** Você como DONO de uma conta, com múltiplos telefones/robôs funcionando.

---

## ✅ PASSO 1: Criar Sua Organização (Tenant)

### **O que é:**
- Sua "conta" no sistema
- É onde seus robôs vão ficar
- Você é o DONO dessa organização

### **Como fazer:**

**Opção A: Via Interface Web**
1. Acesse: `http://localhost:5002/organizations/new`
2. Preencha:
   - **Nome:** "Minha Empresa" (ou o nome que quiser)
   - **Email:** seu email
3. Clique em "Criar"

**Opção B: Via API (mais rápido)**
```bash
curl -X POST http://localhost:5002/api/organizations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Minha Empresa",
    "email": "seu@email.com"
  }'
```

**Resultado:**
- ✅ Organização criada
- ✅ Você é o DONO
- ✅ Anote o `id` da organização (ex: `1`)

---

## ✅ PASSO 2: Criar Múltiplos Robôs (Instâncias)

### **O que é:**
- Cada robô = 1 WhatsApp conectado
- Você pode ter quantos quiser
- Cada um funciona independente

### **Como criar:**

**Opção A: Via Interface Web**
1. Acesse: `http://localhost:5002/instances/new?tenant_id=1` (substitua `1` pelo ID da sua organização)
2. Preencha:
   - **Nome:** "Robô Vendas", "Robô Suporte", etc.
   - **Organização:** Selecione sua organização
3. Clique em "Criar"
4. **Repita para cada robô que quiser**

**Opção B: Via API (mais rápido para vários)**
```bash
# Robô 1
curl -X POST http://localhost:5002/api/instances \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Robô Vendas",
    "tenant_id": 1
  }'

# Robô 2
curl -X POST http://localhost:5002/api/instances \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Robô Suporte",
    "tenant_id": 1
  }'

# Robô 3
curl -X POST http://localhost:5002/api/instances \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Robô Atendimento",
    "tenant_id": 1
  }'

# ... continue para quantos robôs quiser
```

**Resultado:**
- ✅ Cada robô criado tem uma porta diferente (5001, 5002, 5003, etc.)
- ✅ Cada robô está pronto para conectar um WhatsApp
- ✅ Anote o `id` de cada robô

---

## ✅ PASSO 3: Conectar WhatsApp em Cada Robô

### **Para cada robô criado:**

1. **Acesse a página de conexão:**
   - `http://localhost:5002/instances/1/connect` (substitua `1` pelo ID do robô)

2. **Escaneie o QR Code:**
   - Abra WhatsApp no celular
   - Vá em: **Configurações > Aparelhos conectados > Conectar um aparelho**
   - Escaneie o QR Code na tela

3. **Aguarde conexão:**
   - Status muda para "Conectado"
   - Você verá o número do WhatsApp conectado

4. **Repita para cada robô:**
   - Cada robô precisa de um WhatsApp diferente
   - Pode ser:
     - Números diferentes de celular
     - Ou criar contas WhatsApp Business diferentes

**Resultado:**
- ✅ Cada robô conectado ao seu WhatsApp
- ✅ Pronto para receber e enviar mensagens

---

## ✅ PASSO 4: Criar Fluxos de Automação

### **O que é:**
- Fluxos = automações que o robô executa
- Exemplo: "Boas-vindas", "Atendimento com IA", etc.

### **Como criar:**

1. **Acesse:** `http://localhost:5002/flows/new`
2. **Preencha:**
   - **Nome:** "Boas-vindas"
   - **Organização:** Sua organização
   - **Robô:** Selecione qual robô vai usar esse fluxo
   - **Configurações:** Defina o que o fluxo faz
3. **Clique em "Criar"**

**Resultado:**
- ✅ Fluxo criado e ativo
- ✅ Robô vai executar automaticamente

---

## ✅ PASSO 5: Testar Funcionamento

### **Teste básico:**

1. **Envie mensagem para um dos robôs:**
   - Do seu celular, envie mensagem para o WhatsApp conectado
   - Exemplo: "Olá"

2. **Verifique se recebeu:**
   - Acesse: `http://localhost:5002/conversations`
   - Você deve ver a conversa aparecer

3. **Verifique resposta automática:**
   - Se configurou fluxo, o robô deve responder automaticamente
   - Se configurou IA, o robô responde com IA

**Resultado:**
- ✅ Mensagens chegando
- ✅ Respostas automáticas funcionando
- ✅ Sistema operacional

---

## ✅ PASSO 6: Gerenciar Múltiplos Robôs

### **Ver todos os robôs:**
- Acesse: `http://localhost:5002/instances?tenant_id=1`
- Você verá lista de todos os seus robôs
- Status de cada um (Conectado/Desconectado)

### **Ver conversas de cada robô:**
- Acesse: `http://localhost:5002/conversations`
- Filtre por robô (se implementado)
- Ou veja todas as conversas

### **Configurar cada robô:**
- Cada robô pode ter:
  - Seus próprios fluxos
  - Sua própria IA
  - Suas próprias configurações

---

## 📋 CHECKLIST FINAL

- [ ] Organização criada
- [ ] Múltiplos robôs criados
- [ ] WhatsApp conectado em cada robô
- [ ] Fluxos criados e ativos
- [ ] Teste de envio/recebimento funcionando
- [ ] Respostas automáticas funcionando

---

## 🚀 PRÓXIMOS PASSOS (Depois que funcionar)

1. **Adicionar mais robôs** (se precisar)
2. **Criar mais fluxos** (personalizar automações)
3. **Configurar IA** (respostas inteligentes)
4. **Testar em produção** (usar de verdade)
5. **Depois:** Preparar para vender/comercializar

---

## 💡 DICAS

### **Múltiplos WhatsApp:**
- Você pode usar números diferentes
- Ou criar contas WhatsApp Business diferentes
- Cada robô = 1 WhatsApp

### **Organização:**
- Você é DONO da organização
- Não precisa ser ADMIN do sistema
- Foco em usar seus robôs

### **Escalabilidade:**
- Pode criar quantos robôs quiser
- Cada um funciona independente
- Todos na mesma organização

---

**Pronto para começar!** 🎯


