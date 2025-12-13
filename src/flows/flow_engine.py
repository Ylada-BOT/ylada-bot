"""
Motor de Fluxos - Executa automações
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class FlowEngine:
    """
    Motor que executa fluxos de automação
    
    Um fluxo é uma sequência de ações que são executadas quando um trigger é ativado.
    """
    
    def __init__(self):
        self.active_flows: Dict[int, Dict] = {}  # flow_id -> flow_data
        self.flow_executions: Dict[str, Dict] = {}  # execution_id -> execution_data
    
    def load_flow(self, flow_id: int, flow_data: Dict) -> bool:
        """
        Carrega um fluxo para execução
        
        Args:
            flow_id: ID do fluxo
            flow_data: Dados do fluxo (JSON)
        
        Returns:
            True se carregado com sucesso
        """
        try:
            # Valida estrutura do fluxo
            if not self._validate_flow(flow_data):
                logger.error(f"Fluxo {flow_id} inválido")
                return False
            
            self.active_flows[flow_id] = flow_data
            logger.info(f"Fluxo {flow_id} carregado: {flow_data.get('name', 'Sem nome')}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar fluxo {flow_id}: {e}")
            return False
    
    def unload_flow(self, flow_id: int):
        """Remove um fluxo da memória"""
        if flow_id in self.active_flows:
            del self.active_flows[flow_id]
            logger.info(f"Fluxo {flow_id} descarregado")
    
    def _validate_flow(self, flow_data: Dict) -> bool:
        """Valida estrutura do fluxo"""
        required_fields = ['name', 'trigger', 'steps']
        
        for field in required_fields:
            if field not in flow_data:
                logger.error(f"Campo obrigatório ausente: {field}")
                return False
        
        if not isinstance(flow_data['steps'], list):
            logger.error("'steps' deve ser uma lista")
            return False
        
        if len(flow_data['steps']) == 0:
            logger.error("Fluxo deve ter pelo menos um step")
            return False
        
        return True
    
    def check_trigger(self, flow_id: int, message: str, phone: str, **kwargs) -> bool:
        """
        Verifica se um fluxo deve ser executado baseado no trigger
        
        Args:
            flow_id: ID do fluxo
            message: Mensagem recebida
            phone: Número do telefone
            **kwargs: Dados adicionais (conversation_id, etc)
        
        Returns:
            True se o trigger foi ativado
        """
        if flow_id not in self.active_flows:
            return False
        
        flow = self.active_flows[flow_id]
        trigger = flow.get('trigger', {})
        trigger_type = trigger.get('type', 'keyword')
        
        if trigger_type == 'keyword':
            # Trigger por palavras-chave
            keywords = trigger.get('keywords', [])
            message_lower = message.lower()
            
            for keyword in keywords:
                if keyword.lower() in message_lower:
                    logger.info(f"Trigger ativado para fluxo {flow_id}: palavra-chave '{keyword}'")
                    return True
        
        elif trigger_type == 'always':
            # Sempre executa (para fluxos de boas-vindas)
            return True
        
        elif trigger_type == 'condition':
            # Trigger por condição customizada
            condition = trigger.get('condition', {})
            # Implementar lógica de condições depois
            return False
        
        return False
    
    def execute_flow(self, flow_id: int, phone: str, conversation_id: Optional[int] = None, 
                    initial_message: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Executa um fluxo completo
        
        Args:
            flow_id: ID do fluxo
            phone: Número do telefone
            conversation_id: ID da conversa (opcional)
            initial_message: Mensagem inicial que ativou o fluxo
            **kwargs: Dados adicionais
        
        Returns:
            Dict com resultado da execução
        """
        # Atualiza estatísticas no banco
        try:
            from src.database.db import SessionLocal
            from src.models.flow import Flow
            from datetime import datetime
            
            db = SessionLocal()
            try:
                flow = db.query(Flow).filter(Flow.id == flow_id).first()
                if flow:
                    flow.times_executed += 1
                    flow.last_executed_at = datetime.utcnow()
                    db.commit()
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"Erro ao atualizar estatísticas do fluxo {flow_id}: {e}")
        
        # Continua execução normal
        """
        Executa um fluxo completo
        
        Args:
            flow_id: ID do fluxo
            phone: Número do telefone
            conversation_id: ID da conversa (opcional)
            initial_message: Mensagem inicial que ativou o fluxo
            **kwargs: Dados adicionais
        
        Returns:
            Dict com resultado da execução
        """
        if flow_id not in self.active_flows:
            return {
                'success': False,
                'error': f'Fluxo {flow_id} não encontrado'
            }
        
        flow = self.active_flows[flow_id]
        steps = flow.get('steps', [])
        execution_id = f"{flow_id}_{phone}_{datetime.now().timestamp()}"
        
        execution_data = {
            'flow_id': flow_id,
            'phone': phone,
            'conversation_id': conversation_id,
            'started_at': datetime.now(),
            'steps_executed': [],
            'current_step': 0,
            'status': 'running'
        }
        
        self.flow_executions[execution_id] = execution_data
        
        logger.info(f"Iniciando execução do fluxo {flow_id} para {phone}")
        
        try:
            # Obtém whatsapp_handler dos kwargs
            whatsapp_handler = kwargs.get('whatsapp_handler')
            
            # Executa cada step do fluxo
            for step_index, step in enumerate(steps):
                execution_data['current_step'] = step_index
                
                # Remove whatsapp_handler dos kwargs se existir para evitar duplicação
                step_kwargs = {k: v for k, v in kwargs.items() if k != 'whatsapp_handler'}
                step_kwargs['whatsapp_handler'] = whatsapp_handler
                
                result = self._execute_step(
                    step=step,
                    flow_id=flow_id,
                    phone=phone,
                    conversation_id=conversation_id,
                    initial_message=initial_message,
                    execution_data=execution_data,
                    **step_kwargs
                )
                
                execution_data['steps_executed'].append({
                    'step_index': step_index,
                    'step_type': step.get('type'),
                    'result': result,
                    'executed_at': datetime.now()
                })
                
                # Se um step falhar e não for opcional, para a execução
                if not result.get('success', False) and not step.get('optional', False):
                    execution_data['status'] = 'failed'
                    execution_data['error'] = result.get('error', 'Erro desconhecido')
                    logger.error(f"Fluxo {flow_id} falhou no step {step_index}: {result.get('error')}")
                    break
                
                # Se o step indicar que deve parar, para a execução
                if result.get('stop_execution', False):
                    logger.info(f"Fluxo {flow_id} parado pelo step {step_index}")
                    break
            
            execution_data['status'] = 'completed'
            execution_data['completed_at'] = datetime.now()
            
            logger.info(f"Fluxo {flow_id} executado com sucesso para {phone}")
            
            return {
                'success': True,
                'execution_id': execution_id,
                'steps_executed': len(execution_data['steps_executed']),
                'status': 'completed'
            }
            
        except Exception as e:
            execution_data['status'] = 'error'
            execution_data['error'] = str(e)
            logger.error(f"Erro ao executar fluxo {flow_id}: {e}")
            
            return {
                'success': False,
                'error': str(e),
                'execution_id': execution_id
            }
    
    def _execute_step(self, step: Dict, flow_id: int, phone: str, 
                     conversation_id: Optional[int], initial_message: Optional[str],
                     execution_data: Dict, **kwargs) -> Dict[str, Any]:
        """
        Executa um step individual do fluxo
        
        Args:
            step: Dados do step
            flow_id: ID do fluxo
            phone: Número do telefone
            conversation_id: ID da conversa
            initial_message: Mensagem inicial
            execution_data: Dados da execução atual
            **kwargs: Dados adicionais (inclui whatsapp_handler)
        
        Returns:
            Dict com resultado da execução do step
        """
        step_type = step.get('type')
        
        if not step_type:
            return {'success': False, 'error': 'Step sem tipo definido'}
        
        # Importa e executa a ação correspondente
        try:
            if step_type == 'send_message':
                from src.actions.send_message import SendMessageAction
                action = SendMessageAction()
                # Remove whatsapp_handler dos kwargs para evitar duplicação
                step_kwargs = {k: v for k, v in kwargs.items() if k != 'whatsapp_handler'}
                return action.execute(
                    phone=phone, 
                    message=step.get('message', ''),
                    whatsapp_handler=kwargs.get('whatsapp_handler'),
                    **step_kwargs
                )
            
            elif step_type == 'wait':
                from src.actions.wait import WaitAction
                action = WaitAction()
                return action.execute(duration=step.get('duration', 0), **kwargs)
            
            elif step_type == 'condition':
                from src.actions.condition import ConditionAction
                action = ConditionAction()
                return action.execute(
                    condition=step.get('condition', {}),
                    phone=phone,
                    initial_message=initial_message,
                    execution_data=execution_data,
                    **kwargs
                )
            
            elif step_type == 'ai_response':
                from src.actions.ai_response import AIResponseAction
                action = AIResponseAction()
                # Remove whatsapp_handler dos kwargs para evitar duplicação
                step_kwargs = {k: v for k, v in kwargs.items() if k != 'whatsapp_handler'}
                return action.execute(
                    phone=phone,
                    conversation_id=conversation_id,
                    initial_message=initial_message,
                    whatsapp_handler=kwargs.get('whatsapp_handler'),
                    **step_kwargs
                )
            
            elif step_type == 'webhook':
                from src.actions.webhook import WebhookAction
                action = WebhookAction()
                return action.execute(
                    url=step.get('url', ''),
                    method=step.get('method', 'POST'),
                    data=step.get('data', {}),
                    phone=phone,
                    **kwargs
                )
            
            else:
                return {
                    'success': False,
                    'error': f'Tipo de step não suportado: {step_type}'
                }
                
        except ImportError as e:
            logger.error(f"Erro ao importar ação {step_type}: {e}")
            return {
                'success': False,
                'error': f'Ação {step_type} não implementada'
            }
        except Exception as e:
            logger.error(f"Erro ao executar step {step_type}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_active_flows(self) -> List[Dict]:
        """Retorna lista de fluxos ativos"""
        return [
            {
                'flow_id': flow_id,
                'name': flow_data.get('name', 'Sem nome'),
                'trigger': flow_data.get('trigger', {}),
                'steps_count': len(flow_data.get('steps', []))
            }
            for flow_id, flow_data in self.active_flows.items()
        ]


# Instância global do motor de fluxos
flow_engine = FlowEngine()
