"""
APIs de Tenants (Clientes)
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.models.tenant import Tenant, TenantStatus
from src.models.user import User
from src.models.subscription import Subscription, SubscriptionStatus, Plan
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('tenants', __name__, url_prefix='/api/tenants')


def get_current_user_id():
    """Obtém ID do usuário atual da sessão"""
    from flask import session
    return session.get('user_id')


@bp.route('', methods=['POST'])
def create_tenant():
    """Cria novo tenant"""
    try:
        data = request.get_json()
        
        # Validações
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        # Obtém usuário atual
        user_id = get_current_user_id()
        if not user_id:
            # Se não tiver autenticação, usa user_id do request (desenvolvimento)
            user_id = data.get('user_id', 1)
        
        try:
            db = SessionLocal()
        except Exception as db_error:
            logger.error(f"Erro ao conectar com banco de dados: {db_error}")
            return jsonify({
                'error': 'Banco de dados não configurado. Configure o PostgreSQL ou use o modo simples.',
                'hint': 'Para modo simples, acesse /dashboard diretamente (sem tenants)'
            }), 503
        
        try:
            # Verifica se usuário existe (opcional em desenvolvimento)
            user = None
            try:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    # Em desenvolvimento, cria usuário padrão se não existir
                    try:
                        from src.auth.authentication import hash_password
                        from src.models.user import UserRole
                        user = User(
                            id=user_id,
                            email=f'user{user_id}@dev.com',
                            password_hash=hash_password('dev123'),
                            name='Usuário Desenvolvimento',
                            role=UserRole.USER,
                            is_active=True
                        )
                        db.add(user)
                        db.commit()
                        logger.info(f"Usuário {user_id} criado automaticamente (modo dev)")
                    except Exception as e:
                        logger.warning(f"Não foi possível criar usuário: {e}")
                        # Continua mesmo sem usuário (modo dev)
            except Exception as e:
                logger.warning(f"Erro ao verificar usuário: {e}. Continuando em modo dev...")
            
            # Cria tenant
            tenant = Tenant(
                user_id=user_id,
                name=name,
                status=TenantStatus.TRIAL,
                plan_id=data.get('plan_id')  # Opcional
            )
            
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            
            # Cria assinatura se tiver plan_id
            if data.get('plan_id'):
                plan = db.query(Plan).filter(Plan.id == data.get('plan_id')).first()
                if plan:
                    subscription = Subscription(
                        tenant_id=tenant.id,
                        plan_id=plan.id,
                        status=SubscriptionStatus.TRIAL
                    )
                    db.add(subscription)
                    db.commit()
            
            logger.info(f"Tenant criado: {tenant.id} - {tenant.name}")
            
            return jsonify({
                'success': True,
                'tenant': {
                    'id': tenant.id,
                    'name': tenant.name,
                    'status': tenant.status.value,
                    'created_at': tenant.created_at.isoformat()
                }
            }), 201
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao criar tenant: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['GET'])
def list_tenants():
    """Lista tenants do usuário atual"""
    try:
        # Obtém usuário atual
        user_id = get_current_user_id()
        if not user_id:
            # Se não tiver autenticação, lista todos (desenvolvimento)
            user_id = request.args.get('user_id', type=int)
            if not user_id:
                user_id = 1  # Default para desenvolvimento
        
        db = SessionLocal()
        try:
            # Busca tenants do usuário
            tenants = db.query(Tenant).filter(Tenant.user_id == user_id).all()
            
            result = []
            for tenant in tenants:
                # Busca plano e assinatura
                plan = None
                subscription = None
                if tenant.plan_id:
                    plan = db.query(Plan).filter(Plan.id == tenant.plan_id).first()
                subscription = db.query(Subscription).filter(Subscription.tenant_id == tenant.id).first()
                
                result.append({
                    'id': tenant.id,
                    'name': tenant.name,
                    'status': tenant.status.value,
                    'is_blocked': tenant.is_blocked,
                    'plan': {
                        'id': plan.id,
                        'name': plan.name,
                        'price': plan.price
                    } if plan else None,
                    'subscription': {
                        'status': subscription.status.value if subscription else None
                    } if subscription else None,
                    'created_at': tenant.created_at.isoformat(),
                    'instances_count': len(tenant.instances) if tenant.instances else 0
                })
            
            return jsonify({
                'success': True,
                'tenants': result,
                'total': len(result)
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao listar tenants: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:tenant_id>', methods=['GET'])
def get_tenant(tenant_id):
    """Obtém detalhes do tenant"""
    try:
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            
            if not tenant:
                return jsonify({'error': 'Tenant não encontrado'}), 404
            
            # Verifica se usuário tem acesso
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Busca informações relacionadas
            plan = None
            subscription = None
            if tenant.plan_id:
                plan = db.query(Plan).filter(Plan.id == tenant.plan_id).first()
            subscription = db.query(Subscription).filter(Subscription.tenant_id == tenant.id).first()
            
            return jsonify({
                'success': True,
                'tenant': {
                    'id': tenant.id,
                    'name': tenant.name,
                    'status': tenant.status.value,
                    'is_blocked': tenant.is_blocked,
                    'blocked_reason': tenant.blocked_reason,
                    'plan': {
                        'id': plan.id,
                        'name': plan.name,
                        'price': plan.price,
                        'messages_included': plan.messages_included if hasattr(plan, 'messages_included') else None
                    } if plan else None,
                    'subscription': {
                        'id': subscription.id,
                        'status': subscription.status.value,
                        'start_date': subscription.start_date.isoformat() if subscription else None
                    } if subscription else None,
                    'instances': [
                        {
                            'id': inst.id,
                            'name': inst.name,
                            'status': inst.status.value
                        } for inst in tenant.instances
                    ] if tenant.instances else [],
                    'created_at': tenant.created_at.isoformat()
                }
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao obter tenant: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:tenant_id>', methods=['PUT'])
def update_tenant(tenant_id):
    """Atualiza tenant"""
    try:
        data = request.get_json()
        
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            
            if not tenant:
                return jsonify({'error': 'Tenant não encontrado'}), 404
            
            # Verifica se usuário tem acesso
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Atualiza campos
            if 'name' in data:
                tenant.name = data['name']
            if 'status' in data:
                tenant.status = TenantStatus(data['status'])
            if 'plan_id' in data:
                tenant.plan_id = data['plan_id']
            
            tenant.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(tenant)
            
            logger.info(f"Tenant atualizado: {tenant.id}")
            
            return jsonify({
                'success': True,
                'tenant': {
                    'id': tenant.id,
                    'name': tenant.name,
                    'status': tenant.status.value
                }
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atualizar tenant: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:tenant_id>', methods=['DELETE'])
def delete_tenant(tenant_id):
    """Deleta tenant"""
    try:
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            
            if not tenant:
                return jsonify({'error': 'Tenant não encontrado'}), 404
            
            # Verifica se usuário tem acesso
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Deleta tenant (cascade deleta instâncias, fluxos, etc)
            db.delete(tenant)
            db.commit()
            
            logger.info(f"Tenant deletado: {tenant_id}")
            
            return jsonify({
                'success': True,
                'message': 'Tenant deletado com sucesso'
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao deletar tenant: {e}")
        return jsonify({'error': str(e)}), 500

