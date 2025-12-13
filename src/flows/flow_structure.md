# 📋 Estrutura de Fluxos (JSON)

## Formato Padrão

```json
{
  "name": "Nome do Fluxo",
  "description": "Descrição do fluxo",
  "trigger": {
    "type": "keyword",
    "keywords": ["oi", "olá", "bom dia"]
  },
  "steps": [
    {
      "type": "send_message",
      "message": "Olá! Como posso ajudar?"
    },
    {
      "type": "wait",
      "duration": 5
    },
    {
      "type": "ai_response"
    }
  ]
}
```

## Tipos de Trigger

### 1. Keyword (Palavras-chave)
```json
{
  "type": "keyword",
  "keywords": ["oi", "olá", "bom dia", "help"]
}
```

### 2. Always (Sempre)
```json
{
  "type": "always"
}
```

### 3. Condition (Condição)
```json
{
  "type": "condition",
  "condition": {
    "field": "message",
    "operator": "contains",
    "value": "preço"
  }
}
```

## Tipos de Steps (Ações)

### 1. send_message
```json
{
  "type": "send_message",
  "message": "Texto da mensagem"
}
```

### 2. wait
```json
{
  "type": "wait",
  "duration": 10
}
```

### 3. condition
```json
{
  "type": "condition",
  "condition": {
    "type": "contains",
    "field": "message",
    "value": "sim"
  },
  "if_true": [
    {
      "type": "send_message",
      "message": "Ótimo!"
    }
  ],
  "if_false": [
    {
      "type": "send_message",
      "message": "Entendi."
    }
  ]
}
```

### 4. ai_response
```json
{
  "type": "ai_response"
}
```

### 5. webhook
```json
{
  "type": "webhook",
  "url": "https://exemplo.com/webhook",
  "method": "POST",
  "data": {
    "phone": "{{phone}}",
    "message": "{{message}}"
  }
}
```

## Exemplo Completo

```json
{
  "name": "Atendimento Inicial",
  "description": "Fluxo de boas-vindas e triagem",
  "trigger": {
    "type": "keyword",
    "keywords": ["oi", "olá", "bom dia", "boa tarde", "boa noite"]
  },
  "steps": [
    {
      "type": "send_message",
      "message": "Olá! 👋 Bem-vindo! Como posso ajudar você hoje?"
    },
    {
      "type": "wait",
      "duration": 3
    },
    {
      "type": "ai_response"
    }
  ]
}
```
