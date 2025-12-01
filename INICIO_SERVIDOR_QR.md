# 🔧 Como Iniciar o Servidor WhatsApp para QR Code

## Problema: QR Code não aparece

Se o QR Code não está aparecendo, siga estes passos:

## Solução 1: Iniciar Manualmente (Recomendado)

1. **Abra um terminal** na pasta do projeto:
   ```bash
   cd "/Users/air/Ylada BOT"
   ```

2. **Inicie o servidor Node.js manualmente**:
   ```bash
   node whatsapp_server.js
   ```

3. **Aguarde o QR Code aparecer no terminal** (em formato ASCII)

4. **Acesse** http://localhost:5001/qr no navegador

5. **O QR Code deve aparecer na página** após alguns segundos

## Solução 2: Verificar Dependências

Se o servidor não inicia, verifique:

1. **Node.js está instalado?**
   ```bash
   node --version
   ```
   Deve mostrar uma versão (ex: v22.18.0)

2. **Dependências instaladas?**
   ```bash
   npm install
   ```

3. **Porta 3000 está livre?**
   ```bash
   lsof -ti:3000
   ```
   Se retornar um número, a porta está ocupada. Mate o processo:
   ```bash
   lsof -ti:3000 | xargs kill -9
   ```

## Solução 3: Reiniciar Tudo

1. **Pare todos os processos**:
   ```bash
   lsof -ti:3000 | xargs kill -9
   lsof -ti:5001 | xargs kill -9
   ```

2. **Inicie o servidor Node.js**:
   ```bash
   node whatsapp_server.js
   ```

3. **Em outro terminal, inicie o Flask**:
   ```bash
   cd "/Users/air/Ylada BOT"
   source .venv/bin/activate
   python web/app.py
   ```

4. **Acesse** http://localhost:5001/qr

## Como Funciona

- O servidor Node.js roda na **porta 3000**
- O Flask roda na **porta 5001**
- Quando você acessa `/qr`, o Flask tenta iniciar o servidor Node.js automaticamente
- O QR Code é gerado pelo WhatsApp Web.js e aparece:
  - No terminal (formato ASCII)
  - Na página web (imagem)

## Troubleshooting

**"Cannot find module 'whatsapp-web.js'"**
- Execute: `npm install`

**"Port 3000 is already in use"**
- Mate o processo: `lsof -ti:3000 | xargs kill -9`

**QR Code não aparece na página**
- Verifique o terminal onde o servidor Node.js está rodando
- O QR Code em ASCII sempre aparece lá primeiro
- Aguarde alguns segundos e atualize a página

**Servidor não inicia automaticamente**
- Inicie manualmente: `node whatsapp_server.js`
- Depois acesse http://localhost:5001/qr

