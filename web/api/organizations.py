"""
APIs de Organizations (Organizações)
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

bp = Blueprint('organizations', __name__, url_prefix='/api/organizations')


def get_current_user_id():
    """Obtém ID do usuário atual da sessão"""
    from flask import session
    return session.get('user_id')


@bp.route('', methods=['POST'])
def create_organization():
    """Cria nova organização"""
    try:
        data = request.get_json()
        
        # Validações
        name = data.get('name')
        if not name:
            return jsonify({
                'success': False,
                'error': 'Nome é obrigatório'
            }), 400
        
        # MODO SIMPLES: Salva em arquivo JSON (sem banco de dados)
        import json
        import os
        from datetime import datetime
        
        orgs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'organizations.json')
        os.makedirs(os.path.dirname(orgs_file), exist_ok=True)
        
        # Carrega organizações existentes
        organizations = []
        if os.path.exists(orgs_file):
            try:
                with open(orgs_file, 'r', encoding='utf-8') as f:
                    organizations = json.load(f)
            except:
                organizations = []
        
        # Cria nova organização
        new_org = {
            'id': len(organizations) + 1,
            'name': name,
            'status': 'trial',
            'created_at': datetime.now().isoformat(),
            'instances': []
        }
        
        organizations.append(new_org)
        
        # Salva no arquivo
        with open(orgs_file, 'w', encoding='utf-8') as f:
            json.dump(organizations, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Organização criada (modo simples): {new_org['id']} - {new_org['name']}")
        
        return jsonify({
            'success': True,
            'organization': {
                'id': new_org['id'],
                'name': new_org['name'],
                'status': new_org['status'],
                'created_at': new_org['created_at']
            }
        }), 201
        
        # CÓDIGO ANTIGO (com banco de dados) - comentado para usar depois
        """
        # Obtém usuário atual
        user_id = get_current_user_id()
        if not user_id:
            # Se não tiver autenticação, usa user_id do request (desenvolvimento)
            user_id = data.get('user_id', 1)
        
        # Tenta conectar ao banco
        db = None
        try:
            db = SessionLocal()
        except Exception as db_error:
            # Extrai apenas a mensagem principal do erro (sem traceback)
            error_msg = str(db_error)
            error_type = type(db_error).__name__
            
            # Remove traceback completo se houver
            if '\n' in error_msg:
                # Pega apenas a primeira linha (mensagem principal)
                error_msg = error_msg.split('\n')[0]
            
            # Extrai mensagem FATAL se houver
            if 'FATAL:' in error_msg:
                fatal_parts = error_msg.split('FATAL:')
                if len(fatal_parts) > 1:
                    error_msg = 'FATAL: ' + fatal_parts[-1].strip()
            
            logger.error(f"Erro ao conectar com banco de dados: {error_type} - {error_msg}")
            
            # Mensagem mais clara baseada no tipo de erro
            if 'Tenant or user not found' in error_msg or 'password authentication failed' in error_msg:
                return jsonify({
                    'success': False,
                    'error': 'Erro de autenticação no banco de dados',
                    'message': 'A senha ou usuário do banco de dados está incorreto',
                    'hint': 'Verifique a DATABASE_URL no arquivo .env.local. A senha pode ter sido alterada no Supabase.',
                    'solution': '1. Acesse Supabase > Settings > Database\n2. Reset a senha se necessário\n3. Atualize a DATABASE_URL no .env.local'
                }), 503
            elif 'connection' in error_msg.lower() or 'OperationalError' in error_type:
                return jsonify({
                    'success': False,
                    'error': 'Erro de conexão com o banco de dados',
                    'message': 'Não foi possível conectar ao banco de dados',
                    'hint': 'Verifique se a DATABASE_URL está correta e se o projeto Supabase está ativo',
                    'solution': '1. Verifique a connection string no Supabase\n2. Confirme que o projeto está ativo\n3. Teste a conexão'
                }), 503
            else:
                return jsonify({
                    'success': False,
                    'error': 'Banco de dados não configurado',
                    'message': clean_error if len(clean_error) < 200 else 'Configure o PostgreSQL ou use o modo simples',
                    'hint': 'Para modo simples, acesse /dashboard diretamente (sem organizations)'
                }), 503
        
        if not db:
            return jsonify({
                'success': False,
                'error': 'Banco de dados não disponível',
                'message': 'Não foi possível conectar ao banco de dados'
            }), 503
        
        try:
            # Verifica se usuário existe (opcional em desenvolvimento)
            user = None
            try:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    # Em desenvolvimento, busca ou cria primeiro usuário disponível
                    first_user = db.query(User).first()
                    if first_user:
                        user_id = first_user.id
                        user = first_user
                        logger.info(f"Usando usuário existente: ID={user_id}")
                    else:
                        # Cria usuário padrão se não existir nenhum
                        try:
                            from src.models.user import UserRole
                            # Usa hash simples para desenvolvimento
                            user = User(
                                email=f'admin@ylada.com',
                                password_hash='dev_hash_placeholder',
                                name='Admin YLADA',
                                role=UserRole.ADMIN,
                                is_active=True
                            )
                            db.add(user)
                            db.commit()
                            db.refresh(user)
                            user_id = user.id
                            logger.info(f"Usuário admin criado automaticamente: ID={user_id}")
                        except Exception as e:
                            logger.warning(f"Não foi possível criar usuário: {e}")
                            # Tenta usar user_id=1 mesmo sem usuário (pode falhar)
            except Exception as e:
                logger.warning(f"Erro ao verificar usuário: {e}. Continuando em modo dev...")
            
            # Cria tenant (organização)
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
            
            logger.info(f"Organização criada: {tenant.id} - {tenant.name}")
            
            return jsonify({
                'success': True,
                'organization': {
                    'id': tenant.id,
                    'name': tenant.name,
                    'status': tenant.status.value,
                    'created_at': tenant.created_at.isoformat()
                }
            }), 201
            
        finally:
            db.close()
        """
            
    except Exception as e:
        import traceback
        error_msg = str(e)
        logger.error(f"Erro ao criar organização: {e}")
        logger.error(traceback.format_exc())
        
        # Garante que sempre retorna JSON
        return jsonify({
            'success': False,
            'error': 'Erro ao criar organização',
            'message': error_msg,
            'hint': 'Verifique os logs do servidor para mais detalhes'
        }), 500


@bp.route('', methods=['GET'])
def list_organizations():
    """Lista organizações do usuário atual"""
    try:
        # MODO SIMPLES: Lê de arquivo JSON (sem banco de dados)
        import json
        import os
        
        orgs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'organizations.json')
        
        organizations = []
        if os.path.exists(orgs_file):
            try:
                with open(orgs_file, 'r', encoding='utf-8') as f:
                    organizations = json.load(f)
            except:
                organizations = []
        
        # Formata resposta
        result = []
        for org in organizations:
            result.append({
                'id': org.get('id'),
                'name': org.get('name'),
                'status': org.get('status', 'trial'),
                'created_at': org.get('created_at'),
                'instances_count': len(org.get('instances', []))
            })
        
        return jsonify({
            'success': True,
            'organizations': result,
            'total': len(result)
        }), 200
        
        # CÓDIGO COM BANCO DE DADOS (comentado - usar depois quando precisar)
        """
        # Obtém usuário atual
        user_id = get_current_user_id()
        if not user_id:
            user_id = request.args.get('user_id', type=int)
            if not user_id:
                user_id = 1
        
        db = SessionLocal()
        try:
            # Busca tenants (organizações) do usuário
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
                'organizations': result,
                'total': len(result)
            }), 200
            
        finally:
            db.close()
        """
            
    except Exception as e:
        logger.error(f"Erro ao listar organizações: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:organization_id>', methods=['GET'])
def get_organization(organization_id):
    """Obtém detalhes da organização"""
    try:
        # MODO SIMPLES: Lê de arquivo JSON (sem banco de dados)
        import json
        import os
        
        orgs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'organizations.json')
        
        organizations = []
        if os.path.exists(orgs_file):
            try:
                with open(orgs_file, 'r', encoding='utf-8') as f:
                    organizations = json.load(f)
            except:
                organizations = []
        
        # Busca organização pelo ID
        org = None
        for o in organizations:
            if o.get('id') == organization_id:
                org = o
                break
        
        if not org:
            return jsonify({
                'success': False,
                'error': 'Organização não encontrada'
            }), 404
        
        # Formata resposta
        return jsonify({
            'success': True,
            'organization': {
                'id': org.get('id'),
                'name': org.get('name'),
                'status': org.get('status', 'trial'),
                'is_blocked': False,
                'blocked_reason': None,
                'plan': None,
                'subscription': None,
                'instances': org.get('instances', []),
                'created_at': org.get('created_at')
            }
        }), 200
        
        # CÓDIGO COM BANCO DE DADOS (comentado - usar depois quando precisar)
        """
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == organization_id).first()
            
            if not tenant:
                return jsonify({'error': 'Organização não encontrada'}), 404
            
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
                'organization': {
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
        """
            
    except Exception as e:
        logger.error(f"Erro ao obter organização: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao obter organização',
            'message': str(e)
        }), 500


@bp.route('/<int:organization_id>', methods=['PUT'])
def update_organization(organization_id):
    """Atualiza organização"""
    try:
        data = request.get_json()
        
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == organization_id).first()
            
            if not tenant:
                return jsonify({'error': 'Organização não encontrada'}), 404
            
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
            
            logger.info(f"Organização atualizada: {tenant.id}")
            
            return jsonify({
                'success': True,
                'organization': {
                    'id': tenant.id,
                    'name': tenant.name,
                    'status': tenant.status.value
                }
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atualizar organização: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:organization_id>', methods=['DELETE'])
def delete_organization(organization_id):
    """Deleta organização"""
    try:
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == organization_id).first()
            
            if not tenant:
                return jsonify({'error': 'Organização não encontrada'}), 404
            
            # Verifica se usuário tem acesso
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Deleta tenant (cascade deleta instâncias, fluxos, etc)
            db.delete(tenant)
            db.commit()
            
            logger.info(f"Organização deletada: {organization_id}")
            
            return jsonify({
                'success': True,
                'message': 'Organização deletada com sucesso'
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao deletar organização: {e}")
        return jsonify({'error': str(e)}), 500

