# 🔧 Como Corrigir o Fluxo

## ⚠️ Problema Identificado

Você configurou o trigger como **"Sempre (todas as mensagens)"**, o que significa que o bot vai responder "oi" para **QUALQUER mensagem** recebida.

**Exemplo do que vai acontecer:**
- Alguém envia: "Quero comprar" → Bot responde: "oi" ❌
- Alguém envia: "Qual o preço?" → Bot responde: "oi" ❌
- Alguém envia: "oi" → Bot responde: "oi" ✅

## ✅ Solução Recomendada

### **Opção 1: Usar Palavra-chave (Recomendado)**

1. **Mude o Trigger:**
   - De: "Sempre (todas as mensagens)"
   - Para: "Palavra-chave"

2. **Adicione palavras-chave:**
   - "oi"
   - "olá"
   - "ola"
   - "bom dia"
   - "boa tarde"

3. **Mantenha o Step:**
   - Enviar mensagem: "Olá! Como posso ajudar?" (ou outra mensagem melhor)

**Resultado:** Bot só responde quando alguém enviar uma das palavras-chave.

---

### **Opção 2: Melhorar a Mensagem (Se quiser manter "Sempre")**

Se você realmente quer responder TODAS as mensagens, mude a mensagem para algo mais útil:

**Step 1 - Enviar mensagem:**
```
Olá! Recebi sua mensagem. Como posso ajudar você hoje?
```

**⚠️ Atenção:** Isso vai responder TODAS as mensagens, o que pode ser muito invasivo.

---

## 🎯 Recomendação Final

**Use "Palavra-chave" com:**
- Palavras: "oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"
- Mensagem: "Olá! 👋 Bem-vindo ao BOT by YLADA! Como posso ajudar?"

Assim o bot só responde quando alguém cumprimenta, que é o comportamento esperado.
