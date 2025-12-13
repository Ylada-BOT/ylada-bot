# 🧪 Como Testar o Sistema - BOT by YLADA

## ✅ WhatsApp Conectado!

Agora que o WhatsApp está conectado, vamos testar todas as funcionalidades.

---

## 📋 CHECKLIST DE TESTES

### 1. ✅ Verificar Dashboard
- [x] Acesse: `http://localhost:5002`
- [x] Verifique se mostra "✓ Conectado" no card WhatsApp
- [x] Verifique os outros cards (IA, Fluxos, Conversas, Leads, Notificações)

### 2. 🔄 Criar um Fluxo de Automação

1. **Acesse a página de fluxos:**
   - Clique em "Gerenciar Fluxos" no dashboard
   - Ou acesse: `http://localhost:5002/flows`

2. **Criar um fluxo simples:**
   - Clique em "Criar Novo Fluxo"
   - Nome: "Teste de Boas-Vindas"
   - Descrição: "Responde automaticamente a mensagens"
   - Trigger: Palavra-chave "oi" ou "olá"

3. **Adicionar steps:**
   - Step 1: Enviar Mensagem
     - Mensagem: "Olá! Bem-vindo ao BOT by YLADA! Como posso ajudar?"
   - Step 2: (Opcional) Aguardar 2 segundos
   - Step 3: (Opcional) Resposta com IA

4. **Salvar e ativar:**
   - Clique em "Salvar Fluxo"
   - Ative o fluxo

### 3. 📨 Testar Recebimento de Mensagem

1. **Envie uma mensagem para o número conectado:**
   - Use outro WhatsApp
   - Envie: "oi" ou "olá"
   - O fluxo deve responder automaticamente!

2. **Verificar no dashboard:**
   - Card "Conversas" deve mostrar 1 conversa
   - Card "Fluxos" deve mostrar 1 fluxo executado

### 4. 🎯 Verificar Captação de Leads

1. **Envie uma mensagem que indique interesse:**
   - Exemplo: "Quero saber mais sobre o produto"
   - Ou: "Tenho interesse em comprar"

2. **Verificar captura:**
   - Acesse: `http://localhost:5002/leads`
   - Deve aparecer um novo lead capturado
   - Verifique o score de qualificação

### 5. 🔔 Verificar Notificações

1. **Configurar número de destino:**
   - Quando um lead for capturado ou fluxo executado
   - Uma notificação deve ser enviada (se configurado)

2. **Ver notificações:**
   - Acesse: `http://localhost:5002/notifications`
   - Deve mostrar notificações enviadas

### 6. 🤖 Configurar IA (Opcional)

1. **Acesse o dashboard:**
   - Clique em "Configurar IA"
   - Configure OpenAI ou Anthropic
   - Adicione sua API Key

2. **Testar resposta com IA:**
   - Envie uma mensagem que não ative nenhum fluxo
   - A IA deve responder automaticamente

---

## 🎯 TESTE RÁPIDO (5 minutos)

### Passo 1: Criar Fluxo
1. Acesse `/flows/new`
2. Crie um fluxo com trigger "teste"
3. Adicione step: Enviar mensagem "Funcionou!"
4. Salve e ative

### Passo 2: Testar
1. Envie "teste" para o número conectado
2. Deve receber "Funcionou!" automaticamente

### Passo 3: Verificar
1. Dashboard → Ver Leads (deve ter capturado)
2. Dashboard → Ver Notificações (se configurado)

---

## 🐛 PROBLEMAS COMUNS

### Mensagem não é respondida
- Verifique se o fluxo está ativo
- Verifique se o trigger está correto
- Veja os logs do servidor Node.js

### Lead não é capturado
- Verifique se a mensagem tem palavras-chave de interesse
- Veja a página de leads

### Notificação não é enviada
- Verifique se configurou número de destino
- Verifique se WhatsApp está conectado

---

## 📊 PRÓXIMOS PASSOS APÓS TESTES

1. ✅ Criar mais fluxos de automação
2. ✅ Configurar templates prontos
3. ✅ Adicionar mais funcionalidades
4. ✅ Preparar para produção

---

**Status atual:** ✅ WhatsApp conectado e pronto para testes!
