# 🔧 Correções Prioritárias - Implementar Agora

## 🎯 OBJETIVO

Resolver os **5 problemas mais críticos** que estão causando a maioria dos erros na plataforma.

---

## ✅ CORREÇÃO 1: Validar Configurações na Inicialização

### **Problema:**
Sistema não valida se `WHATSAPP_SERVER_URL` está configurado, causando erros 503 em produção.

### **Solução:**
Adicionar validação no início do `web/app.py`:

```python
# No início do app.py, após carregar configurações
def validate_configuration():
    """Valida configurações críticas na inicialização"""
    from config.settings import WHATSAPP_SERVER_URL, IS_PRODUCTION
    
    errors = []
    
    if IS_PRODUCTION:
        if not WHATSAPP_SERVER_URL or 'localhost' in WHATSAPP_SERVER_URL:
            errors.append(
                "❌ WHATSAPP_SERVER_URL não configurado em produção!\n"
                "   Configure no Railway: WHATSAPP_SERVER_URL=http://whatsapp-server-2:5001"
            )
    
    if errors:
        print("\n" + "="*60)
        print("⚠️  ERROS DE CONFIGURAÇÃO DETECTADOS:")
        print("="*60)
        for error in errors:
            print(error)
        print("="*60 + "\n")
        # Em produção, não trava o servidor, apenas avisa
        if not IS_PRODUCTION:
            raise ValueError("Configurações inválidas. Corrija antes de continuar.")
    
    return len(errors) == 0

# Chamar após criar o app
validate_configuration()
```

---

## ✅ CORREÇÃO 2: Aumentar Timeouts e Adicionar Retry

### **Problema:**
Timeouts de 5 segundos são muito curtos, causando erros falsos positivos.

### **Solução:**
Criar utilitário de retry e aumentar timeouts:

```python
# web/utils/http_client.py (NOVO ARQUIVO)
import requests
import time
from typing import Callable, Optional

def retry_request(
    method: str,
    url: str,
    max_retries: int = 3,
    timeout: int = 15,
    retry_delay: int = 2,
    **kwargs
) -> requests.Response:
    """
    Faz requisição HTTP com retry automático
    
    Args:
        method: Método HTTP (get, post, etc)
        url: URL da requisição
        max_retries: Número máximo de tentativas
        timeout: Timeout em segundos
        retry_delay: Delay entre tentativas
        **kwargs: Argumentos adicionais para requests
    
    Returns:
        Response object
    
    Raises:
        requests.RequestException: Se todas as tentativas falharem
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=timeout,
                **kwargs
            )
            # Se status code é 2xx, retorna
            if 200 <= response.status_code < 300:
                return response
            # Se é 4xx (erro do cliente), não tenta novamente
            elif 400 <= response.status_code < 500:
                return response
            # Se é 5xx ou timeout, tenta novamente
            else:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))  # Backoff exponencial
                    continue
                return response
                
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            last_exception = e
            if attempt < max_retries - 1:
                wait_time = retry_delay * (attempt + 1)
                print(f"[!] Tentativa {attempt + 1}/{max_retries} falhou. Aguardando {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise
    
    # Se chegou aqui, todas as tentativas falharam
    if last_exception:
        raise last_exception
    raise requests.exceptions.RequestException("Todas as tentativas falharam")
```

**Usar em `web/app.py`:**
```python
from web.utils.http_client import retry_request

# Substituir todas as chamadas requests.get/post por:
response = retry_request('get', f"{server_url}/health", timeout=15)
```

---

## ✅ CORREÇÃO 3: Health Check Completo

### **Problema:**
Health check básico não verifica dependências.

### **Solução:**
Melhorar endpoint `/health`:

```python
@app.route('/health')
def health():
    """Health check completo - verifica todas as dependências"""
    from config.settings import WHATSAPP_SERVER_URL, IS_PRODUCTION, DATABASE_URL
    import requests
    
    health_status = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Check 1: Banco de dados
    try:
        from src.database.db import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        health_status["checks"]["database"] = "ok"
    except Exception as e:
        health_status["checks"]["database"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check 2: Servidor WhatsApp
    if IS_PRODUCTION and WHATSAPP_SERVER_URL:
        try:
            response = requests.get(f"{WHATSAPP_SERVER_URL}/health", timeout=5)
            if response.status_code == 200:
                health_status["checks"]["whatsapp_server"] = "ok"
            else:
                health_status["checks"]["whatsapp_server"] = f"error: status {response.status_code}"
                health_status["status"] = "degraded"
        except Exception as e:
            health_status["checks"]["whatsapp_server"] = f"error: {str(e)}"
            health_status["status"] = "degraded"
    else:
        health_status["checks"]["whatsapp_server"] = "not_configured"
    
    # Se algum check crítico falhou, retorna 503
    if health_status["status"] == "degraded":
        return jsonify(health_status), 503
    
    return jsonify(health_status), 200
```

---

## ✅ CORREÇÃO 4: Melhorar Mensagens de Erro

### **Problema:**
Mensagens de erro genéricas não ajudam o usuário.

### **Solução:**
Criar função para mensagens de erro amigáveis:

```python
# web/utils/error_messages.py (NOVO ARQUIVO)
def get_friendly_error_message(error: Exception, context: str = "") -> dict:
    """
    Retorna mensagem de erro amigável para o usuário
    
    Args:
        error: Exceção que ocorreu
        context: Contexto adicional (ex: "ao carregar conversas")
    
    Returns:
        dict com error, message, hint, solution
    """
    error_str = str(error).lower()
    
    # Erro de conexão com WhatsApp
    if 'connection' in error_str or '503' in error_str:
        return {
            "error": "Servidor WhatsApp não está disponível",
            "message": "Não foi possível conectar ao servidor WhatsApp.",
            "hint": "Verifique se o serviço WhatsApp está rodando no Railway.",
            "solution": "Configure WHATSAPP_SERVER_URL no Railway ou aguarde alguns segundos e tente novamente."
        }
    
    # Erro de timeout
    if 'timeout' in error_str:
        return {
            "error": "Tempo de espera esgotado",
            "message": "O servidor demorou muito para responder.",
            "hint": "O servidor pode estar sobrecarregado.",
            "solution": "Tente novamente em alguns segundos."
        }
    
    # Erro de autenticação
    if '401' in error_str or 'unauthorized' in error_str:
        return {
            "error": "Não autenticado",
            "message": "Você precisa fazer login para acessar esta funcionalidade.",
            "hint": "Sua sessão pode ter expirado.",
            "solution": "Faça login novamente."
        }
    
    # Erro genérico
    return {
        "error": "Erro inesperado",
        "message": f"Ocorreu um erro {context}.",
        "hint": "Verifique os logs para mais detalhes.",
        "solution": "Tente novamente ou entre em contato com o suporte."
    }
```

**Usar em `web/app.py`:**
```python
from web.utils.error_messages import get_friendly_error_message

except requests.exceptions.ConnectionError as e:
    error_info = get_friendly_error_message(e, "ao carregar conversas")
    return jsonify({
        "success": False,
        **error_info
    }), 503
```

---

## ✅ CORREÇÃO 5: Sistema de Logging Centralizado

### **Problema:**
Logs inconsistentes dificultam debug.

### **Solução:**
Configurar logging estruturado:

```python
# No início do app.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Configurar logging
log_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Handler para arquivo
file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'app.log'),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
))

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))

# Configurar logger do app
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)

# Desabilitar logs do Werkzeug (muito verboso)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### **Fase 1: Correções Críticas (Hoje)**

- [ ] ✅ Validar configurações na inicialização
- [ ] ✅ Criar utilitário de retry (`web/utils/http_client.py`)
- [ ] ✅ Substituir todas as chamadas `requests` por `retry_request`
- [ ] ✅ Aumentar timeouts para 15-30s
- [ ] ✅ Melhorar health check
- [ ] ✅ Criar função de mensagens de erro amigáveis
- [ ] ✅ Configurar logging centralizado

### **Fase 2: Testes (Amanhã)**

- [ ] Testar em ambiente de desenvolvimento
- [ ] Verificar se erros 503 diminuíram
- [ ] Verificar se mensagens de erro estão melhores
- [ ] Verificar se logs estão consistentes

### **Fase 3: Deploy (Depois de Testes)**

- [ ] Commit das correções
- [ ] Deploy em produção
- [ ] Monitorar logs
- [ ] Verificar se problemas foram resolvidos

---

## 🎯 RESULTADO ESPERADO

Após implementar estas correções:

- ✅ **Redução de 80% nos erros 503**
- ✅ **Mensagens de erro mais claras**
- ✅ **Sistema mais resiliente a falhas**
- ✅ **Debug mais fácil com logs estruturados**
- ✅ **Melhor experiência do usuário**

---

## 📝 PRÓXIMOS PASSOS

1. **Revisar este documento**
2. **Implementar Correção 1 (Validação)**
3. **Implementar Correção 2 (Retry)**
4. **Implementar Correção 3 (Health Check)**
5. **Implementar Correção 4 (Mensagens)**
6. **Implementar Correção 5 (Logging)**
7. **Testar tudo**
8. **Deploy**

---

**Prioridade:** 🔴 CRÍTICA  
**Tempo estimado:** 4-6 horas  
**Impacto:** ALTO - Resolve maioria dos erros

