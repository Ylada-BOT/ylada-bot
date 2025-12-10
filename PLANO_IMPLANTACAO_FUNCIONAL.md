# 🚀 Plano de Implantação - Funcionalidades Essenciais

## 🎯 OBJETIVO:
Fazer o bot funcionar **AGORA** para você usar, com:
1. ✅ Sincronizar contatos do WhatsApp
2. ✅ Disparar mensagens
3. ✅ Criar e executar fluxos automatizados
4. ✅ Depois: Adicionar IA para respostas

---

## 📋 FASE 1: CONECTAR WHATSAPP E SINCRONIZAR CONTATOS (Prioridade ALTA)

### **1.1 Conectar WhatsApp via QR Code**
**Status:** ⚠️ Parcial - QR Code funciona, mas precisa conectar
**O que fazer:**
- [x] Página `/qr` existe e funciona
- [ ] Verificar se está conectando corretamente
- [ ] Testar conexão real
- [ ] Salvar sessão para não precisar reconectar sempre

### **1.2 Sincronizar Contatos do WhatsApp**
**Status:** ❌ Não implementado
**O que fazer:**
- [ ] Criar rota `/api/sync-contacts` que:
  - Busca todos os contatos do WhatsApp Web.js
  - Salva no banco de dados (tabela `contacts`)
  - Atualiza informações (nome, telefone)
  - Remove contatos que não existem mais
- [ ] Criar botão no dashboard "Sincronizar Contatos"
- [ ] Mostrar quantos contatos foram sincronizados

**Arquivos a modificar:**
- `web/app.py` - Adicionar rota `/api/sync-contacts`
- `src/database.py` - Métodos para salvar/atualizar contatos
- `web/templates/index_simple.html` - Botão de sincronização

---

## 📋 FASE 2: DISPARAR MENSAGENS (Prioridade ALTA)

### **2.1 Interface de Disparo**
**Status:** ⚠️ Parcial - API existe, mas sem interface
**O que fazer:**
- [ ] Criar página `/broadcast` funcional (não apenas UI)
- [ ] Permitir selecionar contatos
- [ ] Criar template de mensagem
- [ ] Enviar para múltiplos contatos
- [ ] Mostrar progresso (quantos enviados, quantos falharam)
- [ ] Salvar histórico de disparos

**Arquivos a modificar:**
- `web/app.py` - Rota `/api/broadcast` (POST)
- `web/templates/broadcast.html` - Interface funcional
- `src/database.py` - Salvar histórico de campanhas

### **2.2 Envio Individual**
**Status:** ✅ Funciona via API
**O que fazer:**
- [ ] Melhorar interface no dashboard
- [ ] Adicionar campo de busca de contatos
- [ ] Preview da mensagem antes de enviar

---

## 📋 FASE 3: FLUXOS AUTOMATIZADOS (Prioridade MÉDIA)

### **3.1 Executar Fluxos Automaticamente**
**Status:** ⚠️ Parcial - Salva fluxos, mas não executa
**O que fazer:**
- [ ] Criar engine de execução de fluxos
- [ ] Quando receber mensagem, verificar se há fluxo ativo
- [ ] Executar fluxo baseado em palavras-chave ou fluxo padrão
- [ ] Salvar estado do fluxo por contato
- [ ] Permitir múltiplos fluxos simultâneos

**Arquivos a criar:**
- `src/flow_engine.py` - Engine de execução
- `src/flow_state.py` - Gerenciar estado dos fluxos

**Arquivos a modificar:**
- `web/app.py` - Integrar engine no webhook
- `src/bot_simple.py` - Usar engine ao processar mensagens

### **3.2 Construtor de Fluxos Funcional**
**Status:** ⚠️ Parcial - UI existe, mas não executa
**O que fazer:**
- [ ] Melhorar interface do flow builder
- [ ] Permitir criar fluxos visuais
- [ ] Salvar fluxos no banco de dados
- [ ] Ativar/desativar fluxos
- [ ] Testar fluxo antes de ativar

**Arquivos a modificar:**
- `web/templates/flow_builder.html` - Interface funcional
- `web/app.py` - Rotas para salvar/ativar fluxos
- `src/database.py` - Tabela `flows` (se não existir)

### **3.3 Fluxo Exemplo Pronto**
**O que fazer:**
- [ ] Criar fluxo exemplo: "Boas-vindas"
  - Recebe: "oi", "olá", "bom dia"
  - Responde: Mensagem de boas-vindas
  - Pergunta: "Como posso ajudar?"
  - Opções: 1. Informações, 2. Suporte, 3. Vendas
  - Cada opção leva a um fluxo diferente
- [ ] Salvar como template
- [ ] Permitir duplicar e editar

---

## 📋 FASE 4: INTELIGÊNCIA ARTIFICIAL (Prioridade BAIXA - Depois)

### **4.1 Integração com IA**
**O que fazer:**
- [ ] Escolher provider (OpenAI, Anthropic, etc.)
- [ ] Criar wrapper para chamadas de IA
- [ ] Integrar no processamento de mensagens
- [ ] Usar IA quando fluxo não encontrar resposta
- [ ] Salvar contexto da conversa para IA

**Arquivos a criar:**
- `src/ai_handler.py` - Handler de IA
- `config/ai_config.yaml` - Configurações de IA

---

## 🎯 PRIORIZAÇÃO PARA IMPLEMENTAÇÃO IMEDIATA:

### **SPRINT 1 (Hoje - 2-3 horas):**
1. ✅ Sincronizar contatos do WhatsApp
2. ✅ Interface de disparo funcional
3. ✅ Testar envio de mensagens

### **SPRINT 2 (Amanhã - 2-3 horas):**
1. ✅ Engine de fluxos básico
2. ✅ Fluxo exemplo funcionando
3. ✅ Executar fluxos automaticamente

### **SPRINT 3 (Depois):**
1. ✅ Melhorar construtor de fluxos
2. ✅ Adicionar mais fluxos exemplo
3. ✅ Preparar para IA

---

## 📝 CHECKLIST DE IMPLEMENTAÇÃO:

### **Funcionalidades Essenciais:**
- [ ] WhatsApp conectado e funcionando
- [ ] Contatos sincronizados do WhatsApp
- [ ] Disparar mensagens para múltiplos contatos
- [ ] Criar fluxo simples
- [ ] Fluxo executando automaticamente
- [ ] Receber e responder mensagens

### **Interface:**
- [ ] Dashboard mostra contatos sincronizados
- [ ] Botão "Sincronizar Contatos" funcional
- [ ] Página de disparo funcional
- [ ] Construtor de fluxos funcional
- [ ] Visualizar conversas em tempo real

### **Banco de Dados:**
- [ ] Contatos salvos corretamente
- [ ] Histórico de mensagens
- [ ] Fluxos salvos
- [ ] Estado dos fluxos por contato

---

## 🚀 COMEÇAR AGORA:

**Vou implementar na seguinte ordem:**
1. Sincronização de contatos
2. Interface de disparo
3. Engine de fluxos básico
4. Fluxo exemplo

**Pronto para começar?** 🚀

