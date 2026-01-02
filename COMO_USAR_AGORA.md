# 🚀 Como Usar o Sistema Agora - Guia Completo

## ✅ Você já está conectado!

Agora que seu WhatsApp está conectado, você pode configurar o sistema para responder automaticamente.

---

## 📋 PASSO A PASSO

### 1️⃣ **CONFIGURAR A INTELIGÊNCIA ARTIFICIAL**

**O que é?**
- A IA é quem responde quando não há um fluxo específico configurado
- Você pode escolher entre OpenAI (GPT) ou Anthropic (Claude)
- Pode personalizar o comportamento com um "System Prompt"

**Como fazer:**
1. No Dashboard, role até a seção **"Inteligência Artificial"**
2. Clique em **"Configurar IA"**
3. Preencha:
   - **Provider:** Escolha OpenAI ou Anthropic
   - **API Key:** Cole sua chave de API (ex: `sk-...` para OpenAI)
   - **Model:** Escolha o modelo (ex: GPT-4o Mini, Claude 3.5 Sonnet)
   - **System Prompt:** Defina como a IA deve se comportar
     - Exemplo: "Você é um nutricionista profissional e amigável. Sempre responda de forma educada e ofereça ajuda."
4. Clique em **"Salvar Configuração"**

**Onde conseguir API Key:**
- **OpenAI:** https://platform.openai.com/api-keys
- **Anthropic:** https://console.anthropic.com/

---

### 2️⃣ **CRIAR FLUXOS DE AUTOMAÇÃO (OPCIONAL)**

**O que é um Fluxo?**
- É uma automação que responde automaticamente quando certas palavras são ditas
- Exemplo: Quando alguém manda "oi" → responde "Olá! Como posso ajudar?"

**Como criar:**
1. No Dashboard, clique em **"Gerenciar Fluxos"** (ou vá em `/flows`)
2. Clique em **"+ Criar Fluxo"**
3. Configure:
   - **Nome:** Ex: "Boas-vindas"
   - **Palavras-chave:** Ex: "oi", "olá", "bom dia"
   - **Ações:** O que fazer quando ativar
     - Enviar mensagem
     - Aguardar X segundos
     - Usar IA para responder
     - Chamar webhook externo
4. Clique em **"Salvar"**

**Exemplo de Fluxo:**
```json
{
  "name": "Boas-vindas",
  "trigger": {
    "type": "keyword",
    "keywords": ["oi", "olá", "bom dia"]
  },
  "steps": [
    {
      "type": "send_message",
      "message": "Olá! Bem-vindo! Como posso ajudar?"
    }
  ]
}
```

---

### 3️⃣ **COMO FUNCIONA O SISTEMA**

**Fluxo de Resposta Automática:**

```
1. Alguém envia mensagem no WhatsApp
   ↓
2. Sistema verifica se há um FLUXO que corresponde
   (ex: se a mensagem contém "oi" → ativa fluxo "Boas-vindas")
   ↓
3a. Se há FLUXO → Executa o fluxo (envia mensagem configurada)
   ↓
3b. Se NÃO há FLUXO → Usa a IA para responder automaticamente
   ↓
4. Resposta é enviada via WhatsApp
```

**Resumo:**
- ✅ **Fluxos** = Respostas automáticas para situações específicas
- ✅ **IA** = Resposta inteligente quando não há fluxo específico

---

### 4️⃣ **TIPOS DE COMPORTAMENTO (Não há múltiplos robôs no modo simplificado)**

**No modelo simplificado (1 usuário = 1 WhatsApp):**
- Você tem **UM WhatsApp** conectado
- Mas pode criar **MÚLTIPLOS FLUXOS** com comportamentos diferentes
- Cada fluxo pode ter um propósito diferente

**Exemplos de Fluxos:**
1. **Fluxo "Boas-vindas"** → Ativa com "oi", "olá"
2. **Fluxo "Preços"** → Ativa com "preço", "quanto custa"
3. **Fluxo "Agendamento"** → Ativa com "agendar", "marcar"
4. **Fluxo "Cardápio"** → Ativa com "cardápio", "menu"

**Resultado:**
- O mesmo WhatsApp pode ter múltiplos comportamentos
- Dependendo da palavra-chave, um fluxo diferente é ativado
- Se nenhum fluxo ativar, a IA responde

---

### 5️⃣ **TREINAR A IA (System Prompt)**

**O que é System Prompt?**
- É como você "treina" a IA para ter um comportamento específico
- É o contexto que a IA recebe antes de responder

**Exemplos de System Prompt:**

**Para Nutricionista:**
```
Você é uma nutricionista profissional e amigável. 
Sempre responda de forma educada e ofereça ajuda.
Se alguém perguntar sobre dieta, ofereça uma consulta.
Se perguntar sobre preços, mencione os valores dos planos.
```

**Para Vendedor:**
```
Você é um vendedor profissional e persuasivo.
Sempre seja amigável e tente entender a necessidade do cliente.
Se alguém perguntar sobre produtos, liste os principais.
Se perguntar sobre preços, ofereça descontos para novos clientes.
```

**Para Suporte:**
```
Você é um atendente de suporte técnico.
Sempre seja prestativo e tente resolver o problema.
Se não souber a resposta, peça mais informações ou transfira para um humano.
```

**Como configurar:**
1. Vá em **"Configurar IA"** no Dashboard
2. Cole seu System Prompt no campo **"System Prompt"**
3. Salve

---

## 🎯 RESUMO RÁPIDO

1. **WhatsApp:** ✅ Já conectado
2. **Configurar IA:** Dashboard → "Configurar IA" → Preencher API Key e System Prompt
3. **Criar Fluxos (Opcional):** Dashboard → "Gerenciar Fluxos" → Criar automações
4. **Pronto!** O sistema já responde automaticamente

---

## 📞 TESTE AGORA

1. Envie uma mensagem para seu WhatsApp conectado
2. O sistema vai:
   - Verificar se há um fluxo que corresponde
   - Se sim → Executa o fluxo
   - Se não → Usa a IA para responder

---

## ❓ DÚVIDAS COMUNS

**P: Preciso criar fluxos?**
R: Não é obrigatório. Se não criar fluxos, a IA responde tudo automaticamente.

**P: Posso ter múltiplos WhatsApps?**
R: No modo simplificado, cada conta tem 1 WhatsApp. Para múltiplos, seria necessário criar outra conta.

**P: Como mudar o comportamento da IA?**
R: Edite o "System Prompt" em "Configurar IA".

**P: Os fluxos são obrigatórios?**
R: Não. Eles são úteis para respostas automáticas específicas, mas a IA já funciona sozinha.

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Configure a IA (API Key + System Prompt)
2. ✅ Teste enviando uma mensagem
3. ✅ (Opcional) Crie fluxos para situações específicas
4. ✅ Monitore conversas em "Conversas"
5. ✅ Veja leads capturados em "Leads"

**Pronto para começar! 🎉**
