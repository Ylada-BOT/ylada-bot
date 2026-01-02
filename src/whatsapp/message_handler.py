"""
Message Handler - Processa mensagens do WhatsApp e executa fluxos
"""
from typing import Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MessageHandler:
    """
    Handler que processa mensagens recebidas do WhatsApp
    e decide qual fluxo executar
    """
    
    def __init__(self, flow_engine=None):
        """
        Inicializa handler
        
        Args:
            flow_engine: Instância do FlowEngine (opcional)
        """
        if flow_engine:
            self.flow_engine = flow_engine
        else:
            from src.flows.flow_engine import flow_engine
            self.flow_engine = flow_engine
    
    def process_message(self, phone: str, message: str, conversation_id: Optional[int] = None,
                       tenant_id: Optional[int] = None, instance_id: Optional[int] = None, **kwargs) -> Dict:
        """
        Processa uma mensagem recebida
        
        Args:
            phone: Número do telefone
            message: Conteúdo da mensagem
            conversation_id: ID da conversa (opcional)
            tenant_id: ID do tenant (opcional)
            instance_id: ID da instance (telefone) que recebeu a mensagem (opcional)
            **kwargs: Dados adicionais
        
        Returns:
            Dict com resultado do processamento
        """
        try:
            logger.info(f"Processando mensagem de {phone}: {message[:50]}... (instance_id={instance_id})")
            
            # Busca fluxos ativos do tenant (se fornecido)
            # Filtra por instance_id se fornecido
            active_flows = self.flow_engine.get_active_flows(
                tenant_id=tenant_id,
                instance_id=instance_id
            )
            
            if not active_flows:
                logger.info("Nenhum fluxo ativo encontrado")
                return {
                    'processed': False,
                    'reason': 'Nenhum fluxo ativo'
                }
            
            # Verifica qual fluxo deve ser executado
            executed_flows = []
            
            for flow_info in active_flows:
                flow_id = flow_info['flow_id']
                
                # Verifica trigger
                if self.flow_engine.check_trigger(
                    flow_id=flow_id,
                    message=message,
                    phone=phone,
                    conversation_id=conversation_id,
                    tenant_id=tenant_id,
                    **kwargs
                ):
                    # Executa fluxo
                    result = self.flow_engine.execute_flow(
                        flow_id=flow_id,
                        phone=phone,
                        conversation_id=conversation_id,
                        initial_message=message,
                        tenant_id=tenant_id,
                        **kwargs
                    )
                    
                    executed_flows.append({
                        'flow_id': flow_id,
                        'flow_name': flow_info['name'],
                        'result': result
                    })
                    
                    logger.info(f"Fluxo {flow_id} executado para {phone}")
                    
                    # Captura lead se fluxo foi executado
                    if result.get('success'):
                        try:
                            from src.leads.lead_capture import LeadCapture
                            from src.notifications.notification_sender import NotificationSender
                            
                            # Cria capturador de leads
                            notification_sender = None
                            if kwargs.get('notify_to'):
                                notification_sender = NotificationSender(kwargs.get('whatsapp_handler'))
                            
                            lead_capture = LeadCapture(notification_sender=notification_sender)
                            
                            # Captura lead
                            lead = lead_capture.capture_from_flow(
                                tenant_id=tenant_id or 1,
                                phone=phone,
                                message=message,
                                flow_id=flow_id,
                                flow_name=flow_info['name'],
                                conversation_id=conversation_id,
                                notify_to=kwargs.get('notify_to'),
                                notify_to_name=kwargs.get('notify_to_name')
                            )
                            
                            if lead:
                                logger.info(f"Lead {lead.id} capturado do fluxo {flow_id}")
                        except Exception as e:
                            logger.warning(f"Erro ao capturar lead: {e}")
                    
                    # Notifica se fluxo foi executado com sucesso e há número de notificação configurado
                    if result.get('success') and kwargs.get('notify_to'):
                        try:
                            from src.notifications.notification_sender import NotificationSender
                            sender = NotificationSender(kwargs.get('whatsapp_handler'))
                            sender.notify_flow_triggered(
                                tenant_id=tenant_id or 1,
                                flow_id=flow_id,
                                flow_name=flow_info['name'],
                                phone=phone,
                                sent_to=kwargs.get('notify_to'),
                                sent_to_name=kwargs.get('notify_to_name')
                            )
                            logger.info(f"Notificação enviada para {kwargs.get('notify_to')} sobre fluxo {flow_id}")
                        except Exception as e:
                            logger.warning(f"Erro ao enviar notificação: {e}")
            
            # Captura lead mesmo se nenhum fluxo foi executado (captura geral)
            try:
                from src.leads.lead_capture import LeadCapture
                lead_capture = LeadCapture()
                
                # Só captura se a mensagem indicar interesse
                if lead_capture.should_capture(message):
                    lead = lead_capture.capture_from_message(
                        tenant_id=tenant_id or 1,
                        phone=phone,
                        message=message,
                        source='message',
                        conversation_id=conversation_id,
                        notify_to=kwargs.get('notify_to'),
                        notify_to_name=kwargs.get('notify_to_name')
                    )
                    if lead:
                        logger.info(f"Lead {lead.id} capturado de mensagem geral")
            except Exception as e:
                logger.warning(f"Erro ao capturar lead geral: {e}")
            
            if executed_flows:
                return {
                    'processed': True,
                    'flows_executed': executed_flows,
                    'count': len(executed_flows)
                }
            else:
                return {
                    'processed': False,
                    'reason': 'Nenhum trigger ativado'
                }
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return {
                'processed': False,
                'error': str(e)
            }
    
    def load_tenant_flows(self, tenant_id: int, instance_id: Optional[int] = None):
        """
        Carrega fluxos de um tenant específico (e opcionalmente de uma instance)
        
        Args:
            tenant_id: ID do tenant
            instance_id: ID da instance (opcional). Se fornecido, carrega:
                - Fluxos específicos da instance
                - Fluxos compartilhados (instance_id = NULL) do tenant
        """
        try:
            from src.database.db import SessionLocal
            from src.models.flow import Flow, FlowStatus
            from sqlalchemy import or_
            
            db = SessionLocal()
            try:
                # Busca fluxos ativos do tenant
                query = db.query(Flow).filter(
                    Flow.tenant_id == tenant_id,
                    Flow.status == FlowStatus.ACTIVE
                )
                
                if instance_id is not None:
                    # Fluxos específicos da instance OU fluxos compartilhados
                    query = query.filter(
                        or_(
                            Flow.instance_id == instance_id,
                            Flow.instance_id == None
                        )
                    )
                
                flows = query.all()
                
                for flow in flows:
                    if flow.flow_data:
                        self.flow_engine.load_flow(flow.id, flow.flow_data)
                
                logger.info(f"Carregados {len(flows)} fluxos do tenant {tenant_id}" + 
                          (f" para instance {instance_id}" if instance_id else ""))
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Erro ao carregar fluxos do tenant {tenant_id}: {e}")


# Instância global do handler
message_handler = MessageHandler()
