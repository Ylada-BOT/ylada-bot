"""
Action: Aguardar
"""
from typing import Dict, Any
import time
import logging

logger = logging.getLogger(__name__)


class WaitAction:
    """Ação para aguardar um tempo determinado"""
    
    def execute(self, duration: int = 0, **kwargs) -> Dict[str, Any]:
        """
        Aguarda um tempo determinado (em segundos)
        
        Args:
            duration: Tempo em segundos para aguardar
            **kwargs: Dados adicionais
        
        Returns:
            Dict com resultado
        """
        try:
            if duration <= 0:
                return {
                    'success': True,
                    'message': 'Sem espera'
                }
            
            if duration > 300:  # Limite de 5 minutos
                logger.warning(f"Tempo de espera muito longo: {duration}s. Limitando a 300s.")
                duration = 300
            
            logger.info(f"Aguardando {duration} segundos...")
            time.sleep(duration)
            
            return {
                'success': True,
                'message': f'Aguardou {duration} segundos',
                'duration': duration
            }
            
        except Exception as e:
            logger.error(f"Erro ao aguardar: {e}")
            return {
                'success': False,
                'error': str(e)
            }
