"""
APIs Administrativas
Apenas para usuários com role 'admin'
"""
from flask import Blueprint, request, jsonify, session
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def require_admin_api(f):
    """Decorator para exigir que o usuário seja admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica se está logado
        if 'user_id' not in session:
            return jsonify({'error': 'Não autenticado'}), 401
        
        # Verifica se é admin
        user_role = session.get('user_role', 'user')
        if user_role != 'admin':
            return jsonify({'error': 'Acesso negado. Apenas administradores.'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/organizations', methods=['GET'])
@require_admin_api
def list_organizations():
    """Lista todas as organizações (apenas admin)"""
    try:
        from web.api.organizations import list_organizations as org_list
        return org_list()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/users', methods=['GET'])
@require_admin_api
def list_users():
    """Lista todos os usuários (apenas admin)"""
    try:
        users_list = []
        admin_user = None
        
        # Tenta usar banco de dados primeiro
        try:
            from src.database.db import SessionLocal
            from src.models.user import User
            db = SessionLocal()
            try:
                db_users = db.query(User).order_by(User.created_at.desc()).all()
                for user in db_users:
                    user_data = {
                        'id': user.id,
                        'email': user.email,
                        'name': user.name,
                        'role': user.role.value if hasattr(user.role, 'value') else str(user.role),
                        'is_active': user.is_active,
                        'created_at': user.created_at.isoformat() if user.created_at else None,
                        'phone': user.phone,
                        'photo_url': user.photo_url
                    }
                    
                    # Atualiza nome do administrador se for o email correto
                    if user.email == 'faulaandre@gmail.com':
                        user_data['name'] = 'André Paula'
                        admin_user = user_data
                    else:
                        users_list.append(user_data)
            finally:
                db.close()
        except Exception as db_error:
            # Se banco não disponível, usa modo simplificado
            print(f"[!] Erro ao buscar usuários do banco: {db_error}")
            from web.utils.user_helper import _load_users
            users_data = _load_users()
            for user_id, user_data in users_data.items():
                user_info = {
                    'id': user_data.get('id', int(user_id)),
                    'email': user_data.get('email', ''),
                    'name': user_data.get('name', ''),
                    'role': user_data.get('role', 'user'),
                    'is_active': user_data.get('is_active', True),
                    'created_at': user_data.get('created_at', ''),
                    'phone': user_data.get('phone'),
                    'photo_url': user_data.get('photo_url')
                }
                
                # Atualiza nome do administrador se for o email correto
                if user_info['email'] == 'faulaandre@gmail.com':
                    user_info['name'] = 'André Paula'
                    admin_user = user_info
                else:
                    users_list.append(user_info)
        
        # Coloca o administrador no início da lista
        if admin_user:
            users_list.insert(0, admin_user)
        
        return jsonify({
            'success': True,
            'users': users_list,
            'total': len(users_list)
        })
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc() if request.args.get('debug') == 'true' else None
        }), 500

@bp.route('/stats', methods=['GET'])
@require_admin_api
def get_stats():
    """Estatísticas gerais do sistema (apenas admin)"""
    try:
        # TODO: Implementar estatísticas
        return jsonify({
            'success': True,
            'stats': {
                'tenants': 0,
                'users': 0,
                'instances': 0,
                'flows': 0
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


