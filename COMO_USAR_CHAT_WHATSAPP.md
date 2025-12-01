# 💬 Como Usar o Chat do WhatsApp

## Funcionalidade Implementada

Agora você pode ver suas conversas reais do WhatsApp diretamente no dashboard!

## Como Funciona

1. **Botão "Chat" na Sidebar**
   - Clique no botão "💬 Chat" no menu lateral
   - O sistema tentará buscar suas conversas reais do WhatsApp

2. **Conectar WhatsApp**
   - Se ainda não conectou, vá em "📱 Conectar WhatsApp"
   - Escaneie o QR Code com seu celular
   - Aguarde a conexão ser estabelecida

3. **Ver Conversas**
   - Após conectar, clique em "💬 Chat"
   - Suas conversas reais aparecerão no painel esquerdo
   - Mostra: nome, última mensagem, horário, contador de não lidas

## Requisitos

- **Node.js instalado** (para WhatsApp Web.js)
- **Dependências Node.js instaladas**:
  ```bash
  npm install
  ```

## Como Iniciar

1. **Inicie o servidor Flask** (já está rodando):
   ```bash
   python web/app.py
   ```

2. **O servidor Node.js será iniciado automaticamente** quando você:
   - Acessar a página de QR Code (`/qr`)
   - Clicar no botão "Chat" pela primeira vez

3. **Conecte seu WhatsApp**:
   - Vá em `/qr` ou clique em "Conectar WhatsApp"
   - Escaneie o QR Code
   - Aguarde a mensagem "✅ WhatsApp conectado!"

4. **Use o Chat**:
   - Clique em "💬 Chat" na sidebar
   - Suas conversas aparecerão!

## Funcionalidades

✅ **Lista todas as conversas** do seu WhatsApp  
✅ **Mostra última mensagem** de cada conversa  
✅ **Indica mensagens não lidas** com badge azul  
✅ **Diferencia grupos** (ícone 👥)  
✅ **Ordena por mais recente** primeiro  
✅ **Atualiza automaticamente** quando você clica no botão

## Notas

- O servidor Node.js roda na porta **3000**
- O Flask roda na porta **5001**
- Se o WhatsApp não estiver conectado, mostra conversas do bot (modo simples)
- As conversas são buscadas em tempo real do WhatsApp Web.js

## Solução de Problemas

**"Nenhuma conversa ainda"**
- Verifique se o WhatsApp está conectado (veja status em `/qr`)
- Certifique-se de que o servidor Node.js está rodando

**"Erro ao carregar conversas"**
- Verifique se Node.js está instalado: `node --version`
- Instale as dependências: `npm install`
- Reinicie o servidor Flask

**QR Code não aparece**
- O servidor Node.js pode não ter iniciado
- Verifique os logs no terminal
- Tente acessar `/qr` novamente

