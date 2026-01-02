"""
Sistema de Fila de Mensagens para WhatsApp

Garante que mensagens não sejam perdidas mesmo se o servidor cair.
Usa Redis para persistência (ou memória como fallback).
"""
import json
import time
import logging
from typing import Dict, Optional, List
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

# Tenta importar Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis não disponível, usando fila em memória (não persistente)")


class MessageStatus(Enum):
    """Status da mensagem na fila"""
    PENDING = "pending"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"
    RETRYING = "retrying"


class MessageQueue:
    """
    Fila de mensagens para WhatsApp
    
    Funcionalidades:
    - Adiciona mensagens à fila
    - Processa mensagens em ordem
    - Retry automático em falhas
    - Persistência (Redis ou memória)
    """
    
    def __init__(self, redis_url: Optional[str] = None, use_redis: bool = False):
        """
        Inicializa a fila de mensagens
        
        Args:
            redis_url: URL do Redis (ex: redis://localhost:6379/0)
            use_redis: Se True, tenta usar Redis (mesmo se redis_url não fornecido)
        """
        self.use_redis = use_redis and REDIS_AVAILABLE
        self.redis_client = None
        self.memory_queue = []  # Fila em memória (fallback)
        self.memory_processing = {}  # Mensagens sendo processadas
        
        if self.use_redis:
            try:
                if redis_url:
                    self.redis_client = redis.from_url(redis_url, decode_responses=True)
                else:
                    self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
                
                # Testa conexão
                self.redis_client.ping()
                logger.info("✅ Fila de mensagens configurada com Redis")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao conectar Redis, usando memória: {e}")
                self.use_redis = False
                self.redis_client = None
        
        if not self.use_redis:
            logger.info("✅ Fila de mensagens configurada com memória (não persistente)")
    
    def _get_queue_key(self) -> str:
        """Chave da fila no Redis"""
        return "whatsapp:message_queue"
    
    def _get_message_key(self, message_id: str) -> str:
        """Chave de uma mensagem específica no Redis"""
        return f"whatsapp:message:{message_id}"
    
    def _get_processing_key(self) -> str:
        """Chave das mensagens sendo processadas"""
        return "whatsapp:message_processing"
    
    def add_message(
        self,
        phone: str,
        message: str,
        tenant_id: Optional[int] = None,
        instance_id: Optional[int] = None,
        priority: int = 0,
        max_retries: int = 3,
        retry_delay: int = 5
    ) -> str:
        """
        Adiciona mensagem à fila
        
        Args:
            phone: Número de telefone
            message: Mensagem a enviar
            tenant_id: ID do tenant (opcional)
            instance_id: ID da instância/bot (opcional)
            priority: Prioridade (maior = mais prioritário, padrão: 0)
            max_retries: Máximo de tentativas (padrão: 3)
            retry_delay: Delay entre tentativas em segundos (padrão: 5)
        
        Returns:
            message_id: ID único da mensagem
        """
        message_id = f"msg_{int(time.time() * 1000)}_{phone}"
        
        message_data = {
            "id": message_id,
            "phone": phone,
            "message": message,
            "tenant_id": tenant_id,
            "instance_id": instance_id,
            "priority": priority,
            "status": MessageStatus.PENDING.value,
            "created_at": datetime.utcnow().isoformat(),
            "attempts": 0,
            "max_retries": max_retries,
            "retry_delay": retry_delay,
            "last_error": None
        }
        
        if self.use_redis and self.redis_client:
            try:
                # Adiciona à fila ordenada (sorted set) por prioridade
                score = priority * 1000000 + int(time.time())  # Prioridade + timestamp
                self.redis_client.zadd(
                    self._get_queue_key(),
                    {json.dumps(message_data): score}
                )
                
                # Salva mensagem completa
                self.redis_client.set(
                    self._get_message_key(message_id),
                    json.dumps(message_data),
                    ex=86400 * 7  # Expira em 7 dias
                )
                
                logger.info(f"✅ Mensagem {message_id} adicionada à fila (Redis)")
                return message_id
            except Exception as e:
                logger.error(f"❌ Erro ao adicionar mensagem no Redis: {e}")
                # Fallback para memória
                self.use_redis = False
        
        # Fallback: memória
        message_data["score"] = priority * 1000000 + int(time.time())
        self.memory_queue.append(message_data)
        # Ordena por prioridade (maior primeiro)
        self.memory_queue.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        logger.info(f"✅ Mensagem {message_id} adicionada à fila (memória)")
        return message_id
    
    def get_next_message(self) -> Optional[Dict]:
        """
        Obtém próxima mensagem da fila (maior prioridade primeiro)
        
        Returns:
            Dict com dados da mensagem ou None se fila vazia
        """
        if self.use_redis and self.redis_client:
            try:
                # Obtém mensagem com maior score (prioridade)
                result = self.redis_client.zrevrange(self._get_queue_key(), 0, 0, withscores=True)
                
                if not result:
                    return None
                
                message_json, score = result[0]
                message_data = json.loads(message_json)
                
                # Remove da fila e adiciona em processamento
                self.redis_client.zrem(self._get_queue_key(), message_json)
                self.redis_client.sadd(self._get_processing_key(), message_data["id"])
                
                return message_data
            except Exception as e:
                logger.error(f"❌ Erro ao obter mensagem do Redis: {e}")
                return None
        
        # Fallback: memória
        if not self.memory_queue:
            return None
        
        message_data = self.memory_queue.pop(0)
        self.memory_processing[message_data["id"]] = message_data
        return message_data
    
    def mark_sent(self, message_id: str):
        """Marca mensagem como enviada"""
        if self.use_redis and self.redis_client:
            try:
                message_key = self._get_message_key(message_id)
                message_data = self.redis_client.get(message_key)
                
                if message_data:
                    data = json.loads(message_data)
                    data["status"] = MessageStatus.SENT.value
                    data["sent_at"] = datetime.utcnow().isoformat()
                    self.redis_client.set(message_key, json.dumps(data), ex=86400 * 7)
                
                self.redis_client.srem(self._get_processing_key(), message_id)
                logger.info(f"✅ Mensagem {message_id} marcada como enviada")
            except Exception as e:
                logger.error(f"❌ Erro ao marcar mensagem como enviada: {e}")
        else:
            if message_id in self.memory_processing:
                del self.memory_processing[message_id]
            logger.info(f"✅ Mensagem {message_id} marcada como enviada")
    
    def mark_failed(self, message_id: str, error: str, retry: bool = True):
        """
        Marca mensagem como falha e agenda retry se necessário
        
        Args:
            message_id: ID da mensagem
            error: Mensagem de erro
            retry: Se True, agenda retry automático
        """
        if self.use_redis and self.redis_client:
            try:
                message_key = self._get_message_key(message_id)
                message_data = self.redis_client.get(message_key)
                
                if message_data:
                    data = json.loads(message_data)
                    data["attempts"] = data.get("attempts", 0) + 1
                    data["last_error"] = error
                    
                    if retry and data["attempts"] < data.get("max_retries", 3):
                        # Agenda retry
                        data["status"] = MessageStatus.RETRYING.value
                        retry_delay = data.get("retry_delay", 5)
                        score = data.get("priority", 0) * 1000000 + int(time.time()) + retry_delay
                        
                        self.redis_client.zadd(
                            self._get_queue_key(),
                            {json.dumps(data): score}
                        )
                        logger.info(f"🔄 Mensagem {message_id} agendada para retry (tentativa {data['attempts']}/{data.get('max_retries', 3)})")
                    else:
                        # Máximo de tentativas atingido
                        data["status"] = MessageStatus.FAILED.value
                        data["failed_at"] = datetime.utcnow().isoformat()
                        logger.error(f"❌ Mensagem {message_id} falhou após {data['attempts']} tentativas")
                    
                    self.redis_client.set(message_key, json.dumps(data), ex=86400 * 7)
                
                self.redis_client.srem(self._get_processing_key(), message_id)
            except Exception as e:
                logger.error(f"❌ Erro ao marcar mensagem como falha: {e}")
        else:
            if message_id in self.memory_processing:
                data = self.memory_processing[message_id]
                data["attempts"] = data.get("attempts", 0) + 1
                data["last_error"] = error
                
                if retry and data["attempts"] < data.get("max_retries", 3):
                    # Agenda retry
                    data["status"] = MessageStatus.RETRYING.value
                    retry_delay = data.get("retry_delay", 5)
                    data["score"] = data.get("priority", 0) * 1000000 + int(time.time()) + retry_delay
                    self.memory_queue.append(data)
                    self.memory_queue.sort(key=lambda x: x.get("score", 0), reverse=True)
                    logger.info(f"🔄 Mensagem {message_id} agendada para retry (tentativa {data['attempts']}/{data.get('max_retries', 3)})")
                else:
                    data["status"] = MessageStatus.FAILED.value
                    logger.error(f"❌ Mensagem {message_id} falhou após {data['attempts']} tentativas")
                
                del self.memory_processing[message_id]
    
    def get_queue_size(self) -> int:
        """Retorna tamanho da fila"""
        if self.use_redis and self.redis_client:
            try:
                return self.redis_client.zcard(self._get_queue_key())
            except:
                return 0
        return len(self.memory_queue)
    
    def get_processing_count(self) -> int:
        """Retorna número de mensagens sendo processadas"""
        if self.use_redis and self.redis_client:
            try:
                return self.redis_client.scard(self._get_processing_key())
            except:
                return 0
        return len(self.memory_processing)
    
    def clear_queue(self):
        """Limpa a fila (cuidado!)"""
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.delete(self._get_queue_key())
                self.redis_client.delete(self._get_processing_key())
                logger.warning("⚠️ Fila limpa")
            except Exception as e:
                logger.error(f"❌ Erro ao limpar fila: {e}")
        else:
            self.memory_queue.clear()
            self.memory_processing.clear()
            logger.warning("⚠️ Fila limpa")


# Instância global da fila (será inicializada no app.py)
message_queue: Optional[MessageQueue] = None


def init_message_queue(redis_url: Optional[str] = None, use_redis: bool = False) -> MessageQueue:
    """
    Inicializa a fila de mensagens global
    
    Args:
        redis_url: URL do Redis
        use_redis: Se True, tenta usar Redis
    
    Returns:
        Instância da fila
    """
    global message_queue
    message_queue = MessageQueue(redis_url=redis_url, use_redis=use_redis)
    return message_queue


def get_message_queue() -> Optional[MessageQueue]:
    """Obtém instância global da fila"""
    return message_queue



