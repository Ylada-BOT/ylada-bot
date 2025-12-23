# 📝 Mensagem de Commit Sugerida

## Commit Principal

```
feat: Melhorias no sistema de fluxos, integração de conversas e design clean

- ✅ Corrigido carregamento de fluxos do arquivo JSON na inicialização
- ✅ Implementado sistema de persistência em arquivo para fluxos
- ✅ Corrigido erro de whatsapp_handler duplicado no flow engine
- ✅ Melhorado sistema de envio de mensagens com retry logic (3 tentativas)
- ✅ Implementada busca completa de conversas (até 1000 mensagens por chat)
- ✅ Adicionada paginação para mensagens
- ✅ Atualizado design para tons de azul clean e intuitivo
- ✅ Melhorado tratamento de erros e logs detalhados
- ✅ Corrigido relacionamento Lead-Conversation no banco de dados
- ✅ Aplicado padrões da indústria (Twilio/MessageBird) para robustez

Templates atualizados:
- dashboard.html
- conversations/list.html
- flows/list.html
- qr.html
- leads/list.html
- notifications/list.html

Melhorias técnicas:
- Retry automático para envio de mensagens
- Timeout aumentado (15s)
- Busca otimizada de conversas
- Tratamento individual de erros por chat
```

## Arquivos Principais Modificados

- `src/flows/flow_engine.py` - Correção de whatsapp_handler
- `src/whatsapp_webjs_handler.py` - Retry logic e melhorias
- `whatsapp_server.js` - Busca completa de conversas e paginação
- `web/app.py` - Melhorias no webhook e carregamento de fluxos
- `web/api/flows.py` - Persistência em arquivo JSON
- `web/templates/*.html` - Design clean com tons de azul
- `src/models/lead.py` - Correção de relacionamento
