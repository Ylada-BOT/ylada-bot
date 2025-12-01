# 🏗️ Arquitetura do Sistema - Como Funciona

## 📊 Visão Geral

Seu bot tem **2 partes** que funcionam juntas:

### 1️⃣ **API/Web (Vercel)** - ✅ JÁ ESTÁ ONLINE
- **Onde:** Vercel (serverless)
- **O que faz:** 
  - Dashboard web
  - API REST
  - Gerenciamento de contatos/campanhas
  - Armazenamento no Supabase
- **Status:** ✅ Funcionando 24/7 (sempre online)
- **URL:** `https://ylada-bot-8fyl.vercel.app`

### 2️⃣ **WhatsApp Web.js (Servidor)** - ⚠️ PRECISA DE SERVIDOR
- **Onde:** Precisa de servidor dedicado
- **O que faz:**
  - Conecta com WhatsApp
  - Envia/recebe mensagens
  - Mantém sessão ativa
- **Status:** ⚠️ Precisa estar sempre rodando

---

## 🖥️ Opções para WhatsApp Web.js

### Opção 1: Seu Computador (Gratuito) 💻

**Vantagens:**
- ✅ Grátis
- ✅ Controle total
- ✅ Fácil de configurar

**Desvantagens:**
- ❌ Precisa ficar ligado 24/7
- ❌ Se desligar, WhatsApp desconecta
- ❌ Depende da sua internet

**Como usar:**
```bash
# No seu computador
cd "/Users/air/Ylada BOT"
node whatsapp_server.js
```

**Requisitos:**
- Computador ligado 24/7
- Internet estável
- Node.js instalado

---

### Opção 2: Servidor Cloud (Recomendado) ☁️

**Vantagens:**
- ✅ Funciona 24/7 (sempre online)
- ✅ Não depende do seu computador
- ✅ Mais estável
- ✅ Pode reiniciar sem perder conexão

**Desvantagens:**
- 💰 Tem custo (mas barato)

**Opções de Servidor:**

#### A) Railway (Recomendado - Mais Fácil)
- **Custo:** ~$5-10/mês
- **Vantagem:** Muito fácil de configurar
- **Link:** https://railway.app

#### B) Render
- **Custo:** ~$7/mês
- **Vantagem:** Interface simples
- **Link:** https://render.com

#### C) DigitalOcean Droplet
- **Custo:** ~$6/mês
- **Vantagem:** Mais controle
- **Link:** https://digitalocean.com

#### D) AWS EC2
- **Custo:** ~$5-10/mês
- **Vantagem:** Escalável
- **Link:** https://aws.amazon.com/ec2

---

## 🔗 Como Conectam

```
┌─────────────────┐         ┌──────────────────┐
│   Vercel        │         │  Servidor        │
│   (API/Web)     │◄────────┤  WhatsApp Web.js │
│                 │  HTTP   │                  │
│  - Dashboard    │         │  - Envia Msgs    │
│  - API REST     │         │  - Recebe Msgs   │
│  - Supabase     │         │  - QR Code       │
└─────────────────┘         └──────────────────┘
     ✅ Online 24/7              ⚠️ Precisa servidor
```

**Fluxo:**
1. Usuário acessa dashboard no Vercel
2. Vercel faz requisição para servidor WhatsApp
3. Servidor envia mensagem via WhatsApp
4. Resposta volta para Vercel
5. Vercel salva no Supabase

---

## 🎯 Recomendação por Uso

### Para Testes/Desenvolvimento:
- ✅ Use seu computador
- ✅ Rode `node whatsapp_server.js` quando precisar
- ✅ Não precisa ficar 24/7

### Para Produção/Uso Real:
- ✅ Use servidor cloud (Railway ou Render)
- ✅ Deixa rodando 24/7
- ✅ Mais confiável

---

## 📝 Próximos Passos

### Se usar seu computador:
1. Instale Node.js (se não tiver)
2. Rode: `node whatsapp_server.js`
3. Mantenha o terminal aberto
4. Escaneie QR Code quando aparecer

### Se usar servidor cloud:
1. Escolha um provedor (Railway recomendado)
2. Crie conta e projeto
3. Conecte com GitHub
4. Configure para rodar `whatsapp_server.js`
5. Escaneie QR Code no servidor

---

## ⚠️ Importante

- **Vercel:** Já está funcionando ✅
- **WhatsApp:** Precisa de servidor dedicado ⚠️
- **Conexão:** Vercel se comunica com servidor via HTTP
- **Sessão:** WhatsApp precisa estar sempre conectado

---

## 💡 Dica

Para começar, use seu computador para testar. Depois, quando estiver funcionando bem, migre para um servidor cloud para produção.

