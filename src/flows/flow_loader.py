"""
Flow Loader - Carrega fluxos do banco de dados ao iniciar
"""
import logging
from src.database.db import SessionLocal
from src.models.flow import Flow, FlowStatus
from src.flows.flow_engine import flow_engine

logger = logging.getLogger(__name__)


def load_active_flows_from_db(tenant_id: int = None):
    """
    Carrega todos os fluxos ativos do banco de dados
    
    Args:
        tenant_id: ID do tenant (opcional, se None carrega todos)
    
    Returns:
        Número de fluxos carregados
    """
    try:
        db = SessionLocal()
        try:
            # Busca fluxos ativos
            query = db.query(Flow).filter(Flow.status == FlowStatus.ACTIVE)
            
            if tenant_id:
                query = query.filter(Flow.tenant_id == tenant_id)
            
            flows = query.all()
            
            if not flows:
                logger.info("Nenhum fluxo ativo encontrado no banco de dados")
                return 0
            
            loaded_count = 0
            
            for flow in flows:
                try:
                    # Valida e carrega fluxo
                    if flow.flow_data and isinstance(flow.flow_data, dict):
                        success = flow_engine.load_flow(flow.id, flow.flow_data)
                        if success:
                            loaded_count += 1
                            logger.info(f"Fluxo carregado: {flow.name} (ID: {flow.id})")
                        else:
                            logger.warning(f"Falha ao carregar fluxo {flow.id}: estrutura inválida")
                    else:
                        logger.warning(f"Fluxo {flow.id} sem dados válidos")
                        
                except Exception as e:
                    logger.error(f"Erro ao carregar fluxo {flow.id}: {e}")
            
            logger.info(f"Total de fluxos carregados: {loaded_count}/{len(flows)}")
            return loaded_count
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao carregar fluxos do banco: {e}")
        return 0


def reload_flow(flow_id: int):
    """
    Recarrega um fluxo específico do banco
    
    Args:
        flow_id: ID do fluxo
    """
    try:
        db = SessionLocal()
        try:
            flow = db.query(Flow).filter(Flow.id == flow_id).first()
            
            if not flow:
                logger.warning(f"Fluxo {flow_id} não encontrado no banco")
                return False
            
            # Remove da memória se existir
            flow_engine.unload_flow(flow_id)
            
            # Carrega novamente se estiver ativo
            if flow.status == FlowStatus.ACTIVE and flow.flow_data:
                success = flow_engine.load_flow(flow_id, flow.flow_data)
                if success:
                    logger.info(f"Fluxo {flow_id} recarregado")
                    return True
            
            return False
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao recarregar fluxo {flow_id}: {e}")
        return False
