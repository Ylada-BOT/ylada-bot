"""
Rotas de API para gerenciar agentes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.models.agent import Agent
from src.models.instance import Instance
from web.utils.auth_helpers import get_current_tenant_id, get_current_user_id, is_admin
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('agents', __name__, url_prefix='/api/agents')


@bp.route('', methods=['GET'])
def list_agents():
    """Lista todos os agentes"""
    try:
        db = SessionLocal()
        try:
            current_tenant_id = get_current_tenant_id()
            
            if is_admin():
                # Admin vê todos os agentes
                agents = db.query(Agent).all()
            else:
                # Tenant vê apenas seus agentes
                if current_tenant_id:
                    agents = db.query(Agent).filter(Agent.tenant_id == current_tenant_id).all()
                else:
                    agents = []
            
            agents_list = [agent.to_dict() for agent in agents]
            
            return jsonify({
                'success': True,
                'agents': agents_list,
                'total': len(agents_list)
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao listar agentes: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Obtém um agente específico"""
    try:
        db = SessionLocal()
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                return jsonify({'error': 'Agente não encontrado'}), 404
            
            # Verifica permissão
            current_tenant_id = get_current_tenant_id()
            if not is_admin() and agent.tenant_id != current_tenant_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            return jsonify({
                'success': True,
                'agent': agent.to_dict()
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao obter agente: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['POST'])
def create_agent():
    """Cria um novo agente"""
    try:
        data = request.get_json()
        
        # Validações
        name = data.get('name')
        tenant_id = data.get('tenant_id') or get_current_tenant_id()
        instance_id = data.get('instance_id')  # Opcional
        
        if not name:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        if not tenant_id:
            return jsonify({'error': 'tenant_id é obrigatório'}), 400
        
        db = SessionLocal()
        try:
            # Verifica se tenant existe e tem acesso
            from src.models.tenant import Tenant
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant:
                return jsonify({'error': 'Tenant não encontrado'}), 404
            
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id and not is_admin():
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Se instance_id fornecido, verifica se existe e pertence ao tenant
            if instance_id:
                instance = db.query(Instance).filter(
                    Instance.id == instance_id,
                    Instance.tenant_id == tenant_id
                ).first()
                if not instance:
                    return jsonify({'error': 'Instance não encontrada ou não pertence ao tenant'}), 404
            
            # Se is_default=True, remove default de outros agentes
            is_default = data.get('is_default', False)
            if is_default:
                if instance_id:
                    # Remove default de outros agentes da mesma instance
                    db.query(Agent).filter(
                        Agent.instance_id == instance_id,
                        Agent.is_default == True
                    ).update({'is_default': False})
                else:
                    # Remove default de outros agentes do tenant
                    db.query(Agent).filter(
                        Agent.tenant_id == tenant_id,
                        Agent.instance_id == None,
                        Agent.is_default == True
                    ).update({'is_default': False})
            
            # Cria agente
            agent = Agent(
                tenant_id=tenant_id,
                instance_id=instance_id,
                name=name,
                description=data.get('description'),
                provider=data.get('provider', 'openai'),
                model=data.get('model', 'gpt-4o-mini'),
                system_prompt=data.get('system_prompt', 'Você é um assistente útil e amigável.'),
                temperature=data.get('temperature', 0.7),
                max_tokens=data.get('max_tokens', 1000),
                behavior_config=data.get('behavior_config', {}),
                is_default=is_default,
                is_active=data.get('is_active', True)
            )
            
            db.add(agent)
            db.commit()
            db.refresh(agent)
            
            logger.info(f"Agente criado: {agent.id} - {agent.name}")
            
            return jsonify({
                'success': True,
                'agent': agent.to_dict()
            }), 201
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao criar agente: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Atualiza um agente"""
    try:
        data = request.get_json()
        db = SessionLocal()
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                return jsonify({'error': 'Agente não encontrado'}), 404
            
            # Verifica permissão
            current_tenant_id = get_current_tenant_id()
            if not is_admin() and agent.tenant_id != current_tenant_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Atualiza campos
            if 'name' in data:
                agent.name = data['name']
            if 'description' in data:
                agent.description = data.get('description')
            if 'provider' in data:
                agent.provider = data['provider']
            if 'model' in data:
                agent.model = data['model']
            if 'system_prompt' in data:
                agent.system_prompt = data['system_prompt']
            if 'temperature' in data:
                agent.temperature = data['temperature']
            if 'max_tokens' in data:
                agent.max_tokens = data['max_tokens']
            if 'behavior_config' in data:
                agent.behavior_config = data['behavior_config']
            if 'is_active' in data:
                agent.is_active = data['is_active']
            
            # Se is_default mudou
            if 'is_default' in data:
                is_default = data['is_default']
                if is_default and not agent.is_default:
                    # Remove default de outros agentes
                    if agent.instance_id:
                        db.query(Agent).filter(
                            Agent.instance_id == agent.instance_id,
                            Agent.id != agent_id,
                            Agent.is_default == True
                        ).update({'is_default': False})
                    else:
                        db.query(Agent).filter(
                            Agent.tenant_id == agent.tenant_id,
                            Agent.instance_id == None,
                            Agent.id != agent_id,
                            Agent.is_default == True
                        ).update({'is_default': False})
                agent.is_default = is_default
            
            agent.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(agent)
            
            logger.info(f"Agente atualizado: {agent.id} - {agent.name}")
            
            return jsonify({
                'success': True,
                'agent': agent.to_dict()
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atualizar agente: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Remove um agente"""
    try:
        db = SessionLocal()
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                return jsonify({'error': 'Agente não encontrado'}), 404
            
            # Verifica permissão
            current_tenant_id = get_current_tenant_id()
            if not is_admin() and agent.tenant_id != current_tenant_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Verifica se está sendo usado por alguma instance
            instances_using = db.query(Instance).filter(Instance.agent_id == agent_id).count()
            if instances_using > 0:
                return jsonify({
                    'error': f'Agente está sendo usado por {instances_using} instância(s). Remova a associação primeiro.'
                }), 400
            
            db.delete(agent)
            db.commit()
            
            logger.info(f"Agente removido: {agent_id}")
            
            return jsonify({
                'success': True,
                'message': 'Agente removido com sucesso'
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao remover agente: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/by-instance/<int:instance_id>', methods=['GET'])
def get_agent_by_instance(instance_id):
    """Obtém o agente configurado para uma instance"""
    try:
        db = SessionLocal()
        try:
            instance = db.query(Instance).filter(Instance.id == instance_id).first()
            
            if not instance:
                return jsonify({'error': 'Instance não encontrada'}), 404
            
            # Verifica permissão
            current_tenant_id = get_current_tenant_id()
            if not is_admin() and instance.tenant_id != current_tenant_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Busca agente da instance ou agente padrão do tenant
            agent = None
            if instance.agent_id:
                agent = db.query(Agent).filter(Agent.id == instance.agent_id).first()
            
            if not agent:
                # Busca agente padrão do tenant
                agent = db.query(Agent).filter(
                    Agent.tenant_id == instance.tenant_id,
                    Agent.instance_id == None,
                    Agent.is_default == True,
                    Agent.is_active == True
                ).first()
            
            if not agent:
                return jsonify({
                    'success': True,
                    'agent': None,
                    'message': 'Nenhum agente configurado'
                }), 200
            
            return jsonify({
                'success': True,
                'agent': agent.to_dict()
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao obter agente da instance: {e}")
        return jsonify({'error': str(e)}), 500


