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
        # TODO: Implementar listagem de usuários
        return jsonify({
            'success': True,
            'users': []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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


