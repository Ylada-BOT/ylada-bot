# 📱 GUIA PASSO A PASSO - Como Usar o BOT

## ✅ O QUE JÁ ESTÁ FUNCIONANDO

1. ✅ WhatsApp conectado
2. ✅ Conversas sincronizadas (você pode ver todas as conversas)
3. ✅ Sistema de fluxos pronto
4. ✅ Captação de leads pronta
5. ✅ Notificações prontas

---

## 🎯 COMO FUNCIONA (Explicação Simples)

### **Duas Formas de Funcionar:**

#### 1️⃣ **COM FLUXOS (Automação)**
- Você cria um fluxo com regras
- Quando alguém envia "oi", o fluxo responde automaticamente
- **Você precisa criar os fluxos primeiro**

#### 2️⃣ **SEM FLUXOS (IA)**
- Se não tiver fluxo ativo, a IA responde automaticamente
- **Precisa configurar a IA primeiro** (no dashboard)

---

## 📋 PASSO A PASSO COMPLETO

### **PASSO 1: Ver Conversas (Já Funciona!)**

1. Acesse: `http://localhost:5002/conversations`
2. Você verá TODAS as conversas do seu WhatsApp
3. Clique em uma conversa para ver as mensagens
4. **Isso já está funcionando!** ✅

**O que aparece:**
- Todas as conversas do seu WhatsApp
- Mensagens antigas e novas
- Contatos sincronizados automaticamente

---

### **PASSO 2: Criar um Fluxo de Automação**

**O que é um fluxo?**
- É uma regra que diz: "Quando alguém enviar X, responda Y"

**Como criar:**

1. **Acesse a página de fluxos:**
   - No dashboard, clique em "Gerenciar Fluxos"
   - Ou acesse: `http://localhost:5002/flows`

2. **Clique em "Criar Novo Fluxo"**

3. **Preencha:**
   - **Nome:** "Boas-Vindas"
   - **Descrição:** "Responde quando alguém diz oi"
   - **Trigger:** Escolha "Palavra-chave"
   - **Palavras-chave:** Digite "oi" (pode adicionar mais: "olá", "ola")

4. **Adicione um Step (Ação):**
   - Clique em "Adicionar Step"
   - Escolha: "Enviar Mensagem"
   - Digite a mensagem: "Olá! Bem-vindo ao BOT by YLADA! Como posso ajudar?"

5. **Salve:**
   - Clique em "Salvar Fluxo"
   - O fluxo será ativado automaticamente

---

### **PASSO 3: Testar o Fluxo**

1. **Use outro WhatsApp** (ou peça para alguém)
2. **Envie "oi"** para o número conectado
3. **O bot deve responder automaticamente!** ✅

**O que acontece:**
- ✅ Mensagem recebida
- ✅ Fluxo detecta a palavra "oi"
- ✅ Bot responde automaticamente
- ✅ Lead é capturado (se a mensagem indicar interesse)
- ✅ Notificação é enviada (se configurado)

---

### **PASSO 4: Ver os Resultados**

1. **Dashboard:**
   - Card "Fluxos" → Mostra quantos fluxos foram executados
   - Card "Conversas" → Mostra conversas ativas
   - Card "Leads" → Mostra leads capturados

2. **Página de Leads:**
   - Acesse: `http://localhost:5002/leads`
   - Veja todos os leads capturados
   - Veja o score de qualificação

3. **Página de Notificações:**
   - Acesse: `http://localhost:5002/notifications`
   - Veja todas as notificações enviadas

---

## 🔄 FLUXO COMPLETO (Resumo)

```
1. Alguém envia mensagem → WhatsApp recebe
2. Sistema verifica se há fluxo ativo
   ├─ Se SIM → Executa o fluxo → Responde automaticamente
   └─ Se NÃO → Usa IA (se configurada) → Responde automaticamente
3. Sistema captura lead (se indicar interesse)
4. Sistema envia notificação (se configurado)
5. Tudo aparece no dashboard e páginas
```

---

## ❓ PERGUNTAS FREQUENTES

### **P: As conversas antigas aparecem?**
**R:** Sim! Todas as conversas do seu WhatsApp aparecem na página de conversas.

### **P: Preciso criar fluxo para cada conversa?**
**R:** Não! Um fluxo funciona para TODAS as conversas. Se alguém enviar "oi", o fluxo responde.

### **P: E se não criar fluxo?**
**R:** Se você configurar a IA no dashboard, ela responde automaticamente. Se não configurar, nada acontece.

### **P: Como saber se funcionou?**
**R:** 
- Veja a página de conversas (mensagem aparece)
- Veja a página de leads (lead foi capturado)
- Veja o dashboard (estatísticas atualizadas)

### **P: Posso criar vários fluxos?**
**R:** Sim! Crie quantos quiser:
- Fluxo "Boas-Vindas" → responde "oi"
- Fluxo "Preços" → responde sobre preços
- Fluxo "Contato" → envia número de contato
- etc.

---

## 🎯 TESTE RÁPIDO (5 minutos)

1. ✅ Acesse `/conversations` → Veja suas conversas
2. ✅ Acesse `/flows/new` → Crie um fluxo com trigger "teste"
3. ✅ Envie "teste" para o número conectado
4. ✅ Veja a resposta automática
5. ✅ Acesse `/leads` → Veja o lead capturado

---

## 📊 RESUMO

**O que você tem agora:**
- ✅ WhatsApp conectado
- ✅ Ver todas as conversas
- ✅ Criar fluxos de automação
- ✅ Captar leads automaticamente
- ✅ Receber notificações

**O que fazer:**
1. Ver conversas → Já funciona! ✅
2. Criar fluxos → Você precisa criar
3. Testar → Enviar mensagem e ver funcionar

**Próximo passo:**
👉 Criar seu primeiro fluxo e testar!
