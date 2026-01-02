"""
Worker para processar fila de mensagens do WhatsApp

Este worker roda em background e processa mensagens da fila continuamente.
"""
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class MessageWorker:
    """
    Worker que processa mensagens da fila
    
    Funcionalidades:
    - Processa mensagens em ordem de prioridade
    - Retry automático em falhas
    - Rate limiting integrado
    - Logs detalhados
    """
    
    def __init__(self, message_queue, whatsapp_handler, interval: float = 1.0):
        """
        Inicializa o worker
        
        Args:
            message_queue: Instância de MessageQueue
            whatsapp_handler: Handler do WhatsApp (WhatsAppWebJSHandler)
            interval: Intervalo entre processamentos em segundos (padrão: 1.0)
        """
        self.message_queue = message_queue
        self.whatsapp_handler = whatsapp_handler
        self.interval = interval
        self.running = False
        self.processed_count = 0
        self.failed_count = 0
    
    def start(self):
        """Inicia o worker"""
        if self.running:
            logger.warning("⚠️ Worker já está rodando")
            return
        
        self.running = True
        logger.info("🚀 Worker de mensagens iniciado")
        
        try:
            while self.running:
                self._process_next_message()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("⏹️ Worker interrompido pelo usuário")
        except Exception as e:
            logger.error(f"❌ Erro no worker: {e}")
        finally:
            self.running = False
            logger.info("⏹️ Worker parado")
    
    def stop(self):
        """Para o worker"""
        self.running = False
        logger.info("⏹️ Parando worker...")
    
    def _process_next_message(self):
        """Processa próxima mensagem da fila"""
        try:
            # Obtém próxima mensagem
            message = self.message_queue.get_next_message()
            
            if not message:
                # Fila vazia, aguarda
                return
            
            message_id = message.get("id")
            phone = message.get("phone")
            message_text = message.get("message")
            
            logger.info(f"📤 Processando mensagem {message_id} para {phone}")
            
            # Verifica se WhatsApp está conectado
            if not self.whatsapp_handler or not self.whatsapp_handler.is_ready():
                error = "WhatsApp não está conectado"
                logger.warning(f"⚠️ {error}")
                self.message_queue.mark_failed(message_id, error, retry=True)
                self.failed_count += 1
                return
            
            # Envia mensagem
            try:
                success = self.whatsapp_handler.send_message(phone, message_text)
                
                if success:
                    self.message_queue.mark_sent(message_id)
                    self.processed_count += 1
                    logger.info(f"✅ Mensagem {message_id} enviada com sucesso")
                else:
                    error = "Falha ao enviar mensagem (retorno False)"
                    logger.warning(f"⚠️ {error}")
                    self.message_queue.mark_failed(message_id, error, retry=True)
                    self.failed_count += 1
                    
            except Exception as e:
                error = f"Erro ao enviar mensagem: {str(e)}"
                logger.error(f"❌ {error}")
                self.message_queue.mark_failed(message_id, error, retry=True)
                self.failed_count += 1
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar mensagem: {e}")
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do worker"""
        return {
            "running": self.running,
            "processed": self.processed_count,
            "failed": self.failed_count,
            "queue_size": self.message_queue.get_queue_size() if self.message_queue else 0,
            "processing": self.message_queue.get_processing_count() if self.message_queue else 0
        }


# Instância global do worker (será inicializada no app.py)
message_worker: Optional[MessageWorker] = None


def init_message_worker(message_queue, whatsapp_handler, interval: float = 1.0) -> MessageWorker:
    """
    Inicializa o worker de mensagens global
    
    Args:
        message_queue: Instância de MessageQueue
        whatsapp_handler: Handler do WhatsApp
        interval: Intervalo entre processamentos
    
    Returns:
        Instância do worker
    """
    global message_worker
    message_worker = MessageWorker(message_queue, whatsapp_handler, interval)
    return message_worker


def get_message_worker() -> Optional[MessageWorker]:
    """Obtém instância global do worker"""
    return message_worker



