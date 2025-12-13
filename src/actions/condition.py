"""
Action: Condição (If/Else)
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConditionAction:
    """Ação para executar lógica condicional"""
    
    def execute(self, condition: Dict, phone: str, initial_message: Optional[str] = None,
               execution_data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        Avalia uma condição e retorna resultado
        
        Args:
            condition: Dict com a condição a avaliar
            phone: Número do telefone
            initial_message: Mensagem inicial
            execution_data: Dados da execução atual
            **kwargs: Dados adicionais
        
        Returns:
            Dict com resultado (inclui 'condition_met' para indicar se condição foi atendida)
        """
        try:
            condition_type = condition.get('type', 'contains')
            field = condition.get('field', 'message')
            value = condition.get('value', '')
            
            # Obtém o valor a comparar
            if field == 'message':
                text_to_check = initial_message or ''
            elif field == 'phone':
                text_to_check = phone
            else:
                # Tenta obter do execution_data ou kwargs
                text_to_check = str(execution_data.get(field, '') if execution_data else kwargs.get(field, ''))
            
            # Avalia condição
            condition_met = False
            
            if condition_type == 'contains':
                condition_met = value.lower() in text_to_check.lower()
            
            elif condition_type == 'equals':
                condition_met = text_to_check.lower() == value.lower()
            
            elif condition_type == 'starts_with':
                condition_met = text_to_check.lower().startswith(value.lower())
            
            elif condition_type == 'ends_with':
                condition_met = text_to_check.lower().endswith(value.lower())
            
            elif condition_type == 'not_contains':
                condition_met = value.lower() not in text_to_check.lower()
            
            logger.info(f"Condição '{condition_type}' avaliada: {condition_met}")
            
            return {
                'success': True,
                'condition_met': condition_met,
                'condition_type': condition_type,
                'field': field,
                'value': value
            }
            
        except Exception as e:
            logger.error(f"Erro ao avaliar condição: {e}")
            return {
                'success': False,
                'error': str(e),
                'condition_met': False
            }
