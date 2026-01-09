"""
Rotas de autenticação
"""
from flask import Blueprint, request, jsonify, session
import os
import jwt
from datetime import datetime, timedelta

# Tenta importar banco de dados, mas não falha se não estiver configurado
DB_AVAILABLE = False
try:
    from sqlalchemy.orm import Session
    from src.database.db import SessionLocal
    from src.auth.authentication import (
        register_user, authenticate_user, create_token, get_user_by_id
    )
    from src.models.user import UserRole
    # Testa conexão antes de marcar como disponível
    try:
        db = SessionLocal()
        db.close()
        DB_AVAILABLE = True
        print("[✓] Banco de dados disponível")
    except Exception as db_error:
        DB_AVAILABLE = False
        print(f"[!] Banco de dados não disponível (erro de conexão): {db_error}")
        print("[!] Sistema funcionará em modo simplificado (arquivo JSON)")
except Exception as e:
    # Modo desenvolvimento sem banco de dados
    DB_AVAILABLE = False
    print(f"[!] Banco de dados não disponível: {e}")
    print("[!] Sistema funcionará em modo simplificado (arquivo JSON)")

# Importa helpers simplificados
try:
    from web.utils.user_helper import (
        register_user_simple, authenticate_user_simple, get_user_by_id_simple
    )
    SIMPLE_AUTH_AVAILABLE = True
except Exception as e:
    SIMPLE_AUTH_AVAILABLE = False
    print(f"[!] Helpers simplificados não disponíveis: {e}")

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Configuração JWT simples - usa JWT_SECRET_KEY de settings.py
from config.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS
JWT_SECRET = os.getenv('JWT_SECRET_KEY', JWT_SECRET_KEY)


def create_token_simple(user_id: int, email: str, role: str) -> str:
    """Cria token JWT simples"""
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


@bp.route('/setup', methods=['POST'])
def setup_first_user():
    """Cria primeiro usuário do sistema (apenas se não houver usuários)"""
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', 'Admin')
        
        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Verifica se já existe usuário
        if SIMPLE_AUTH_AVAILABLE:
            # Carrega usuários do arquivo
            import json
            import os
            users_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users.json')
            users = {}
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r', encoding='utf-8') as f:
                        users = json.load(f)
                except:
                    users = {}
            
            if users:
                return jsonify({'error': 'Sistema já possui usuários. Use /register para criar novos.'}), 400
            
            # Cria primeiro usuário
            user = register_user_simple(email, password, name)
            if user:
                token = create_token_simple(user['id'], user['email'], user['role'])
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                session['user_role'] = user['role']
                
                return jsonify({
                    'success': True,
                    'message': 'Primeiro usuário criado com sucesso!',
                    'token': token,
                    'user': user
                }), 201
        
        return jsonify({'error': 'Sistema de autenticação não disponível'}), 503
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/register', methods=['POST'])
def register():
    """Registra novo usuário"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        
        if not email or not password or not name:
            return jsonify({'error': 'Email, senha e nome são obrigatórios'}), 400
        
        # Tenta usar banco de dados se disponível
        if DB_AVAILABLE:
            try:
                db = SessionLocal()
                try:
                    user = register_user(db, email, password, name, UserRole.USER)
                    
                    if not user:
                        # Se não criou no banco, tenta modo simplificado
                        if SIMPLE_AUTH_AVAILABLE:
                            user = register_user_simple(email, password, name)
                            if not user:
                                return jsonify({'error': 'Email já cadastrado'}), 400
                            
                            token = create_token_simple(user['id'], user['email'], user['role'])
                            session['user_id'] = user['id']
                            session['user_email'] = user['email']
                            session['user_role'] = user['role']
                            
                            return jsonify({
                                'success': True,
                                'message': 'Usuário criado com sucesso',
                                'token': token,
                                'user': {
                                    'id': user['id'],
                                    'email': user['email'],
                                    'name': user['name'],
                                    'role': user['role']
                                }
                            }), 201
                        return jsonify({'error': 'Email já cadastrado'}), 400
                    
                    # Cria token
                    token = create_token(user.id, user.email, user.role.value)
                    
                    # Salva na sessão
                    session['user_id'] = user.id
                    session['user_email'] = user.email
                    session['user_role'] = user.role.value
                
                    return jsonify({
                        'success': True,
                        'message': 'Usuário criado com sucesso',
                        'token': token,
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'name': user.name,
                            'role': user.role.value
                        }
                    }), 201
                finally:
                    db.close()
            except Exception as db_error:
                # Se erro de conexão, usa modo simplificado como fallback
                print(f"[!] Erro ao conectar com banco: {db_error}")
                if SIMPLE_AUTH_AVAILABLE:
                    user = register_user_simple(email, password, name)
                    if not user:
                        return jsonify({'error': 'Email já cadastrado'}), 400
                    
                    token = create_token_simple(user['id'], user['email'], user['role'])
                    session['user_id'] = user['id']
                    session['user_email'] = user['email']
                    session['user_role'] = user['role']
                    
                    return jsonify({
                        'success': True,
                        'message': 'Usuário criado com sucesso (modo simplificado)',
                        'token': token,
                        'user': {
                            'id': user['id'],
                            'email': user['email'],
                            'name': user['name'],
                            'role': user['role']
                        }
                    }), 201
                else:
                    return jsonify({
                        'error': f'Erro de conexão com banco de dados: {str(db_error)}'
                    }), 503
        
        # Modo simplificado (arquivo JSON)
        elif SIMPLE_AUTH_AVAILABLE:
            user = register_user_simple(email, password, name)
            
            if not user:
                return jsonify({'error': 'Email já cadastrado'}), 400
            
            # Verifica se usuário foi salvo corretamente antes de criar token
            import json
            import os
            users_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users.json')
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r', encoding='utf-8') as f:
                        saved_users = json.load(f)
                        if str(user['id']) not in saved_users:
                            return jsonify({
                                'error': 'Erro ao salvar usuário',
                                'hint': 'Tente novamente ou verifique permissões do servidor'
                            }), 500
                except Exception as e:
                    print(f"[!] Erro ao verificar salvamento: {e}")
            
            # Cria token
            token = create_token_simple(user['id'], user['email'], user['role'])
            
            # Salva na sessão
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            
            return jsonify({
                'success': True,
                'message': 'Usuário criado com sucesso',
                'token': token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'role': user['role']
                }
            }), 201
        
        else:
            return jsonify({
                'error': 'Sistema de autenticação não disponível'
            }), 503
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Login de usuário"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        print(f"[DEBUG LOGIN] Tentando login para: {email}")
        print(f"[DEBUG LOGIN] DB_AVAILABLE: {DB_AVAILABLE}")
        print(f"[DEBUG LOGIN] SIMPLE_AUTH_AVAILABLE: {SIMPLE_AUTH_AVAILABLE}")
        
        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Tenta usar banco de dados se disponível
        if DB_AVAILABLE:
            try:
                db = SessionLocal()
                try:
                    print(f"[DEBUG LOGIN] Tentando autenticar no banco de dados...")
                    user = authenticate_user(db, email, password)
                    
                    if not user:
                        print(f"[DEBUG LOGIN] Usuário não encontrado no banco, tentando modo simplificado...")
                        # Se não encontrou no banco, tenta modo simplificado
                        if SIMPLE_AUTH_AVAILABLE:
                            user = authenticate_user_simple(email, password)
                            if user:
                                # Se encontrou no arquivo JSON, cria no banco para sincronizar
                                print(f"[DEBUG LOGIN] Usuário encontrado no arquivo JSON, criando no banco...")
                                try:
                                    from src.auth.authentication import register_user
                                    from src.models.user import UserRole
                                    # Tenta criar no banco (pode falhar se já existir, mas não importa)
                                    try:
                                        new_user = register_user(
                                            db, 
                                            email=user['email'],
                                            password=password,  # Precisa da senha original
                                            name=user['name'],
                                            role=UserRole[user['role'].upper()] if user['role'].upper() in ['ADMIN', 'RESELLER', 'USER'] else UserRole.USER
                                        )
                                        print(f"[✓] Usuário sincronizado do JSON para o banco")
                                    except Exception as create_error:
                                        # Se falhar (ex: usuário já existe), continua com autenticação do JSON
                                        print(f"[!] Não foi possível criar no banco (pode já existir): {create_error}")
                                except Exception as sync_error:
                                    print(f"[!] Erro ao sincronizar usuário: {sync_error}")
                                
                                # Continua com autenticação do JSON
                                token = create_token_simple(user['id'], user['email'], user['role'])
                                session['user_id'] = user['id']
                                session['user_email'] = user['email']
                                session['user_role'] = user['role']
                                
                                return jsonify({
                                    'success': True,
                                    'token': token,
                                    'user': {
                                        'id': user['id'],
                                        'email': user['email'],
                                        'name': user['name'],
                                        'role': user['role']
                                    }
                                }), 200
                            
                            if not user:
                                print(f"[DEBUG LOGIN] Falha na autenticação simplificada também")
                                # Em produção, se o arquivo JSON não existe, tenta criar no banco
                                import os
                                from config.settings import IS_PRODUCTION
                                if IS_PRODUCTION:
                                    print(f"[DEBUG LOGIN] Em produção, tentando criar usuário no banco...")
                                    try:
                                        from src.auth.authentication import register_user
                                        from src.models.user import UserRole
                                        # Tenta criar no banco
                                        new_user = register_user(
                                            db,
                                            email=email,
                                            password=password,
                                            name=email.split('@')[0].upper(),
                                            role=UserRole.USER
                                        )
                                        if new_user:
                                            print(f"[✓] Usuário criado no banco em produção")
                                            # Autentica o usuário recém-criado
                                            user = authenticate_user(db, email, password)
                                    except Exception as create_error:
                                        print(f"[!] Erro ao criar usuário no banco: {create_error}")
                                
                                if not user:
                                    return jsonify({
                                        'error': 'Credenciais inválidas',
                                        'hint': 'Verifique se o email e senha estão corretos. Email: ' + email
                                    }), 401
                            
                            # Cria token simplificado
                            token = create_token_simple(user['id'], user['email'], user['role'])
                            session['user_id'] = user['id']
                            session['user_email'] = user['email']
                            session['user_role'] = user['role']
                            
                            return jsonify({
                                'success': True,
                                'token': token,
                                'user': {
                                    'id': user['id'],
                                    'email': user['email'],
                                    'name': user['name'],
                                    'role': user['role']
                                }
                            }), 200
                        return jsonify({'error': 'Credenciais inválidas'}), 401
                    
                    # Cria token
                    token = create_token(user.id, user.email, user.role.value)
                    
                    # Salva na sessão
                    session['user_id'] = user.id
                    session['user_email'] = user.email
                    session['user_role'] = user.role.value
                
                    return jsonify({
                        'success': True,
                        'token': token,
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'name': user.name,
                            'role': user.role.value
                        }
                    }), 200
                finally:
                    db.close()
            except Exception as db_error:
                # Se erro de conexão, usa modo simplificado como fallback
                print(f"[!] Erro ao conectar com banco: {db_error}")
                print(f"[DEBUG LOGIN] Usando modo simplificado como fallback...")
                if SIMPLE_AUTH_AVAILABLE:
                    user = authenticate_user_simple(email, password)
                    if not user:
                        print(f"[DEBUG LOGIN] Falha na autenticação simplificada após erro de banco")
                        return jsonify({
                            'error': 'Credenciais inválidas',
                            'hint': 'Verifique se o email e senha estão corretos. Email: ' + email
                        }), 401
                    
                    token = create_token_simple(user['id'], user['email'], user['role'])
                    session['user_id'] = user['id']
                    session['user_email'] = user['email']
                    session['user_role'] = user['role']
                    
                    return jsonify({
                        'success': True,
                        'token': token,
                        'user': {
                            'id': user['id'],
                            'email': user['email'],
                            'name': user['name'],
                            'role': user['role']
                        }
                    }), 200
                else:
                    return jsonify({
                        'error': f'Erro de conexão com banco de dados: {str(db_error)}'
                    }), 503
        
        # Modo simplificado (arquivo JSON)
        elif SIMPLE_AUTH_AVAILABLE:
            try:
                print(f"[DEBUG LOGIN] Tentando autenticar no modo simplificado: {email}")
                user = authenticate_user_simple(email, password)
                
                if not user:
                    # Debug: verifica se usuário existe
                    import json
                    import os
                    from pathlib import Path
                    users_file = Path(__file__).resolve().parent.parent.parent / 'data' / 'users.json'
                    print(f"[DEBUG LOGIN] Arquivo de usuários: {users_file}")
                    print(f"[DEBUG LOGIN] Arquivo existe: {users_file.exists()}")
                    
                    if users_file.exists():
                        try:
                            with open(users_file, 'r', encoding='utf-8') as f:
                                users = json.load(f)
                                print(f"[DEBUG LOGIN] Total de usuários no arquivo: {len(users)}")
                                # Verifica se email existe
                                email_found = False
                                for u in users.values():
                                    user_email = u.get('email', '').lower().strip()
                                    if user_email == email.lower().strip():
                                        email_found = True
                                        print(f"[DEBUG LOGIN] Email encontrado: {user_email}")
                                        print(f"[DEBUG LOGIN] Role do usuário: {u.get('role')}")
                                        break
                                
                                if not email_found:
                                    print(f"[DEBUG LOGIN] Email não encontrado no arquivo")
                                    return jsonify({
                                        'error': 'Email não encontrado',
                                        'hint': 'Verifique se o usuário foi criado. Use /register para criar uma conta.'
                                    }), 401
                        except Exception as file_error:
                            print(f"[!] Erro ao ler arquivo de usuários: {file_error}")
                    else:
                        print(f"[DEBUG LOGIN] Arquivo de usuários não existe! Criando...")
                        # Tenta criar arquivo vazio
                        try:
                            users_file.parent.mkdir(parents=True, exist_ok=True)
                            with open(users_file, 'w', encoding='utf-8') as f:
                                json.dump({}, f)
                            print(f"[✓] Arquivo de usuários criado")
                        except Exception as create_error:
                            print(f"[!] Erro ao criar arquivo: {create_error}")
                    
                    return jsonify({
                        'error': 'Credenciais inválidas',
                        'hint': 'Verifique se a senha está correta ou se o usuário existe. Use /register para criar uma conta.'
                    }), 401
            except Exception as auth_error:
                print(f"[!] Erro na autenticação: {auth_error}")
                return jsonify({
                    'error': 'Erro ao autenticar',
                    'details': str(auth_error) if app.debug else None
                }), 500
            
            # Cria token
            token = create_token_simple(user['id'], user['email'], user['role'])
            
            # Salva na sessão
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            
            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'role': user['role']
                }
            }), 200
        
        else:
            return jsonify({
                'error': 'Sistema de autenticação não disponível'
            }), 503
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/me', methods=['GET'])
def get_current_user():
    """Obtém usuário atual"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    # Tenta usar banco de dados se disponível
    if DB_AVAILABLE:
        try:
            db = SessionLocal()
            try:
                user = get_user_by_id(db, user_id)
                
                if not user:
                    return jsonify({'error': 'Usuário não encontrado'}), 404
                
                return jsonify({
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'phone': user.phone or '',
                    'photo_url': user.photo_url or '',
                    'role': user.role.value,
                    'is_active': user.is_active
                }), 200
            finally:
                db.close()
        except:
            pass
    
    # Modo simplificado (arquivo JSON)
    if SIMPLE_AUTH_AVAILABLE:
        user = get_user_by_id_simple(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'phone': user.get('phone', ''),
            'photo_url': user.get('photo_url', ''),
            'role': user['role'],
            'is_active': user.get('is_active', True)
        }), 200
    
    return jsonify({'error': 'Sistema de autenticação não disponível'}), 503


@bp.route('/profile', methods=['GET', 'PUT'])
def profile():
    """Obtém ou atualiza perfil do usuário"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    if request.method == 'GET':
        # Retorna dados do perfil (mesma lógica de /me)
        return get_current_user()
    
    # PUT - Atualiza perfil
    try:
        data = request.get_json()
        
        # Tenta usar banco de dados se disponível
        if DB_AVAILABLE:
            try:
                db = SessionLocal()
                try:
                    user = get_user_by_id(db, user_id)
                    
                    if not user:
                        return jsonify({'error': 'Usuário não encontrado'}), 404
                    
                    # Atualiza campos permitidos
                    if 'name' in data:
                        user.name = data['name'].strip()
                    if 'phone' in data:
                        user.phone = data['phone'].strip() if data['phone'] else None
                    if 'photo_url' in data:
                        user.photo_url = data['photo_url'].strip() if data['photo_url'] else None
                    
                    db.commit()
                    db.refresh(user)
                    
                    return jsonify({
                        'success': True,
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'name': user.name,
                            'phone': user.phone or '',
                            'photo_url': user.photo_url or '',
                            'role': user.role.value
                        }
                    }), 200
                finally:
                    db.close()
            except Exception as db_error:
                error_msg = str(db_error)
                # Verifica se é erro de coluna não encontrada
                if 'column' in error_msg.lower() and 'does not exist' in error_msg.lower():
                    return jsonify({
                        'error': 'Colunas de perfil não encontradas no banco de dados',
                        'details': 'As colunas phone e photo_url não existem na tabela users. Execute o script SQL: scripts/add_user_profile_fields.sql no Supabase.',
                        'hint': 'Acesse o Supabase > SQL Editor > Execute o script add_user_profile_fields.sql',
                        'original_error': error_msg
                    }), 500
                return jsonify({'error': f'Erro ao atualizar perfil: {error_msg}'}), 500
        
        # Modo simplificado (arquivo JSON)
        if SIMPLE_AUTH_AVAILABLE:
            import json
            import os
            from pathlib import Path
            
            users_file = Path(__file__).resolve().parent.parent.parent / 'data' / 'users.json'
            users_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Carrega usuários
            users = []
            if users_file.exists():
                try:
                    with open(users_file, 'r', encoding='utf-8') as f:
                        users = json.load(f)
                except:
                    users = []
            
            # Busca e atualiza usuário
            user = None
            for u in users:
                if u.get('id') == user_id:
                    user = u
                    break
            
            if not user:
                return jsonify({'error': 'Usuário não encontrado'}), 404
            
            # Atualiza campos
            if 'name' in data:
                user['name'] = data['name'].strip()
            if 'phone' in data:
                user['phone'] = data['phone'].strip() if data.get('phone') else ''
            if 'photo_url' in data:
                user['photo_url'] = data['photo_url'].strip() if data.get('photo_url') else ''
            
            # Salva
            with open(users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'phone': user.get('phone', ''),
                    'photo_url': user.get('photo_url', ''),
                    'role': user['role']
                }
            }), 200
        
        return jsonify({'error': 'Sistema de autenticação não disponível'}), 503
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/profile/upload-photo', methods=['POST'])
def upload_photo():
    """Faz upload da foto de perfil"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    try:
        from flask import current_app
        from werkzeug.utils import secure_filename
        from pathlib import Path
        import uuid
        from config.settings import UPLOAD_FOLDER, MAX_UPLOAD_SIZE
        
        # Verifica se arquivo foi enviado
        if 'photo' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['photo']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Valida tipo de arquivo
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        filename = secure_filename(file.filename)
        if '.' not in filename:
            return jsonify({'error': 'Arquivo sem extensão'}), 400
        
        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in allowed_extensions:
            return jsonify({'error': f'Tipo de arquivo não permitido. Use: {", ".join(allowed_extensions)}'}), 400
        
        # Verifica tamanho
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_UPLOAD_SIZE:
            return jsonify({'error': f'Arquivo muito grande. Máximo: {MAX_UPLOAD_SIZE // 1024 // 1024}MB'}), 400
        
        # Cria diretório de uploads se não existir
        upload_dir = Path(UPLOAD_FOLDER) / 'profiles'
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Gera nome único para o arquivo
        unique_filename = f"{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
        file_path = upload_dir / unique_filename
        
        # Salva arquivo
        file.save(str(file_path))
        
        # Gera URL relativa (ajusta caminho baseado na estrutura)
        # O arquivo será servido via rota /static/uploads/<path:filename>
        photo_url = f"/static/uploads/profiles/{unique_filename}"
        
        # Atualiza photo_url no banco/arquivo
        if DB_AVAILABLE:
            try:
                db = SessionLocal()
                try:
                    user = get_user_by_id(db, user_id)
                    if user:
                        user.photo_url = photo_url
                        db.commit()
                    else:
                        file_path.unlink()
                        return jsonify({'error': 'Usuário não encontrado'}), 404
                finally:
                    db.close()
            except Exception as db_error:
                file_path.unlink()
                error_msg = str(db_error)
                # Verifica se é erro de coluna não encontrada
                if 'column' in error_msg.lower() and 'does not exist' in error_msg.lower():
                    return jsonify({
                        'error': 'Colunas de perfil não encontradas no banco de dados',
                        'details': 'As colunas phone e photo_url não existem na tabela users. Execute o script SQL: scripts/add_user_profile_fields.sql no Supabase.',
                        'hint': 'Acesse o Supabase > SQL Editor > Execute o script add_user_profile_fields.sql',
                        'original_error': error_msg
                    }), 500
                return jsonify({'error': f'Erro ao atualizar perfil: {error_msg}'}), 500
        elif SIMPLE_AUTH_AVAILABLE:
            import json
            from pathlib import Path
            
            users_file = Path(__file__).resolve().parent.parent.parent / 'data' / 'users.json'
            users_file.parent.mkdir(parents=True, exist_ok=True)
            
            users = []
            if users_file.exists():
                try:
                    with open(users_file, 'r', encoding='utf-8') as f:
                        users = json.load(f)
                except:
                    users = []
            
            user = None
            for u in users:
                if u.get('id') == user_id:
                    user = u
                    break
            
            if user:
                user['photo_url'] = photo_url
                with open(users_file, 'w', encoding='utf-8') as f:
                    json.dump(users, f, indent=2, ensure_ascii=False)
            else:
                file_path.unlink()
                return jsonify({'error': 'Usuário não encontrado'}), 404
        else:
            file_path.unlink()
            return jsonify({'error': 'Sistema de autenticação não disponível'}), 503
        
        return jsonify({
            'success': True,
            'photo_url': photo_url,
            'message': 'Foto enviada com sucesso'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao fazer upload: {str(e)}'}), 500


@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Endpoint temporário para resetar senha (apenas para portalmagra)"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        new_password = data.get('password', '').strip()
        
        if not email or not new_password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Apenas para portalmagra por segurança
        if email.lower() != 'portalmagra@gmail.com':
            return jsonify({'error': 'Este endpoint é apenas para portalmagra@gmail.com'}), 403
        
        if DB_AVAILABLE:
            try:
                from src.auth.authentication import hash_password
                from src.models.user import User
                db = SessionLocal()
                try:
                    user = db.query(User).filter(User.email == email.lower()).first()
                    if not user:
                        return jsonify({'error': 'Usuário não encontrado'}), 404
                    
                    # Atualiza senha com hash bcrypt
                    user.password_hash = hash_password(new_password)
                    db.commit()
                    
                    return jsonify({
                        'success': True,
                        'message': 'Senha atualizada com sucesso!'
                    }), 200
                finally:
                    db.close()
            except Exception as e:
                return jsonify({'error': f'Erro ao atualizar senha: {str(e)}'}), 500
        
        return jsonify({'error': 'Banco de dados não disponível'}), 503
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
