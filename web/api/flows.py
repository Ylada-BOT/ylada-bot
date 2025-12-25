"""
Rotas de API para gerenciar fluxos
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from src.database.db import SessionLocal, get_db
from src.models.flow import Flow, FlowStatus
from src.flows.flow_engine import flow_engine
from src.whatsapp.message_handler import message_handler
from web.utils.auth_helpers import get_current_tenant_id, is_admin
from datetime import datetime
import json

bp = Blueprint('flows', __name__, url_prefix='/api/flows')


@bp.route('', methods=['GET'])
def list_flows():
    """Lista todos os fluxos"""
    try:
        # Tenta buscar do banco de dados
        try:
            db = SessionLocal()
            try:
                # Filtra por tenant_id (admin vê todos, tenant vê só seus)
                current_tenant_id = get_current_tenant_id()
                if is_admin():
                    # Admin vê todos os fluxos
                    flows = db.query(Flow).all()
                else:
                    # Tenant vê apenas seus fluxos
                    if current_tenant_id:
                        flows = db.query(Flow).filter(Flow.tenant_id == current_tenant_id).all()
                    else:
                        flows = []  # Sem tenant, sem fluxos
                
                flows_list = []
                for flow in flows:
                    flows_list.append({
                        'flow_id': flow.id,
                        'flow_name': flow.name,
                        'description': flow.description,
                        'status': flow.status.value,
                        'trigger': flow.trigger_keywords or [],
                        'steps_count': len(flow.flow_data.get('steps', [])) if isinstance(flow.flow_data, dict) else 0,
                        'times_executed': flow.times_executed,
                        'last_executed_at': flow.last_executed_at.isoformat() if flow.last_executed_at else None,
                        'created_at': flow.created_at.isoformat() if flow.created_at else None
                    })
                
                return jsonify({
                    'success': True,
                    'flows': flows_list,
                    'total': len(flows_list),
                    'source': 'database'
                }), 200
                
            finally:
                db.close()
                
        except Exception as db_error:
            # Fallback: retorna fluxos da memória se banco não disponível
            print(f"[!] Erro ao buscar do banco: {db_error}")
            active_flows = flow_engine.get_active_flows()
            
            return jsonify({
                'success': True,
                'flows': active_flows,
                'total': len(active_flows),
                'source': 'memory',
                'warning': 'Banco de dados não disponível, usando memória'
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['POST'])
def create_flow():
    """Cria um novo fluxo"""
    try:
        data = request.get_json()
        
        # Valida dados
        if not data.get('name') and not data.get('flow_data', {}).get('name'):
            return jsonify({'error': 'Nome do fluxo é obrigatório'}), 400
        
        flow_data = data.get('flow_data', {})
        if not flow_data:
            return jsonify({'error': 'Dados do fluxo são obrigatórios'}), 400
        
        # Valida estrutura do fluxo
        if not flow_engine._validate_flow(flow_data):
            return jsonify({'error': 'Estrutura do fluxo inválida'}), 400
        
        # Tenta salvar no banco de dados
        try:
            db = SessionLocal()
            try:
                # Extrai trigger keywords se for tipo keyword
                trigger_keywords = []
                if flow_data.get('trigger', {}).get('type') == 'keyword':
                    trigger_keywords = flow_data['trigger'].get('keywords', [])
                
                # Obtém tenant_id (por enquanto usa 1, depois pegar do usuário logado)
                tenant_id = data.get('tenant_id', 1)
                
                # Se tenant_id=1 não existir, cria um tenant padrão
                try:
                    from src.models.tenant import Tenant
                    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
                    if not tenant:
                        # Cria tenant padrão se não existir
                        from src.models.user import User, UserRole
                        user = db.query(User).first()
                        if not user:
                            # Cria usuário padrão
                            from src.auth.authentication import hash_password
                            user = User(
                                email='default@ylada.com',
                                password_hash=hash_password('default123'),
                                name='Usuário Padrão',
                                role=UserRole.USER
                            )
                            db.add(user)
                            db.commit()
                            db.refresh(user)
                        
                        tenant = Tenant(
                            user_id=user.id,
                            name='Tenant Padrão',
                            status='active'
                        )
                        db.add(tenant)
                        db.commit()
                        db.refresh(tenant)
                        tenant_id = tenant.id
                except Exception as e:
                    print(f"[!] Erro ao verificar tenant: {e}")
                    # Continua com tenant_id=1 mesmo se der erro
                
                # Cria fluxo no banco
                flow = Flow(
                    tenant_id=tenant_id,
                    name=flow_data.get('name', data.get('name', 'Sem nome')),
                    description=flow_data.get('description', ''),
                    flow_data=flow_data,
                    status=FlowStatus.ACTIVE,
                    trigger_keywords=trigger_keywords,
                    is_template=False
                )
                
                db.add(flow)
                db.commit()
                db.refresh(flow)
                
                # Carrega no motor de fluxos (se estiver ativo)
                if flow.status == FlowStatus.ACTIVE:
                    flow_engine.load_flow(flow.id, flow_data)
                
                return jsonify({
                    'success': True,
                    'message': 'Fluxo criado e ativado com sucesso',
                    'flow_id': flow.id,
                    'flow': {
                        'id': flow.id,
                        'name': flow.name,
                        'status': flow.status.value
                    }
                }), 201
                
            finally:
                db.close()
                
        except Exception as db_error:
            # Fallback: salva em arquivo JSON se banco não disponível
            print(f"[!] Erro ao salvar no banco: {db_error}")
            
            try:
                import json
                import os
                flows_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'flows_memory.json')
                os.makedirs(os.path.dirname(flows_file), exist_ok=True)
                
                # Carrega fluxos existentes
                if os.path.exists(flows_file):
                    with open(flows_file, 'r') as f:
                        flows_data = json.load(f)
                else:
                    flows_data = {'flows': []}
                
                # Gera novo ID
                flow_id = max([f.get('id', 0) for f in flows_data.get('flows', [])] + [0]) + 1
                
                # Adiciona novo fluxo
                new_flow = {
                    'id': flow_id,
                    'name': flow_data.get('name', data.get('name', 'Sem nome')),
                    'description': flow_data.get('description', ''),
                    'flow_data': flow_data,
                    'status': 'active',
                    'created_at': datetime.now().isoformat()
                }
                flows_data['flows'].append(new_flow)
                
                # Salva no arquivo
                with open(flows_file, 'w') as f:
                    json.dump(flows_data, f, indent=2)
                
                # Carrega no motor
                success = flow_engine.load_flow(flow_id, flow_data)
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': 'Fluxo criado e salvo em arquivo (banco não disponível)',
                        'flow_id': flow_id,
                        'warning': 'Banco de dados não disponível, fluxo salvo em arquivo'
                    }), 201
                else:
                    return jsonify({'error': 'Erro ao carregar fluxo na memória'}), 500
                    
            except Exception as file_error:
                print(f"[!] Erro ao salvar em arquivo: {file_error}")
                # Último recurso: apenas memória
                flow_id = len(flow_engine.active_flows) + 1
                success = flow_engine.load_flow(flow_id, flow_data)
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': 'Fluxo criado apenas na memória (será perdido ao reiniciar)',
                        'flow_id': flow_id,
                        'warning': 'Banco e arquivo não disponíveis, fluxo apenas na memória'
                    }), 201
                else:
                    return jsonify({'error': 'Erro ao criar fluxo'}), 500
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:flow_id>', methods=['GET'])
def get_flow(flow_id):
    """Obtém um fluxo específico"""
    try:
        # Tenta buscar do banco
        try:
            db = SessionLocal()
            try:
                flow = db.query(Flow).filter(Flow.id == flow_id).first()
                
                if not flow:
                    return jsonify({'error': 'Fluxo não encontrado'}), 404
                
                return jsonify({
                    'success': True,
                    'flow_id': flow.id,
                    'flow': {
                        'id': flow.id,
                        'name': flow.name,
                        'description': flow.description,
                        'flow_data': flow.flow_data,
                        'status': flow.status.value,
                        'trigger_keywords': flow.trigger_keywords,
                        'times_executed': flow.times_executed,
                        'last_executed_at': flow.last_executed_at.isoformat() if flow.last_executed_at else None
                    }
                }), 200
                
            finally:
                db.close()
                
        except Exception:
            # Fallback: busca da memória
            if flow_id not in flow_engine.active_flows:
                return jsonify({'error': 'Fluxo não encontrado'}), 404
            
            flow = flow_engine.active_flows[flow_id]
            
            return jsonify({
                'success': True,
                'flow_id': flow_id,
                'flow': flow,
                'source': 'memory'
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:flow_id>', methods=['DELETE'])
def delete_flow(flow_id):
    """Remove um fluxo"""
    try:
        # Tenta remover do banco
        try:
            db = SessionLocal()
            try:
                flow = db.query(Flow).filter(Flow.id == flow_id).first()
                
                if not flow:
                    return jsonify({'error': 'Fluxo não encontrado'}), 404
                
                # Remove do banco
                db.delete(flow)
                db.commit()
                
                # Remove da memória
                flow_engine.unload_flow(flow_id)
                
                return jsonify({
                    'success': True,
                    'message': 'Fluxo removido com sucesso'
                }), 200
                
            finally:
                db.close()
                
        except Exception as db_error:
            # Fallback: remove apenas da memória
            print(f"[!] Erro ao remover do banco: {db_error}")
            
            if flow_id not in flow_engine.active_flows:
                return jsonify({'error': 'Fluxo não encontrado'}), 404
            
            flow_engine.unload_flow(flow_id)
            
            return jsonify({
                'success': True,
                'message': 'Fluxo removido da memória (banco não disponível)',
                'warning': 'Banco de dados não disponível'
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/test', methods=['POST'])
def test_flow():
    """Testa um fluxo sem salvar"""
    try:
        data = request.get_json()
        
        # Suporta tanto flow_data quanto flow_id
        if data.get('flow_id'):
            # Testa fluxo existente
            flow_id = data['flow_id']
            if flow_id not in flow_engine.active_flows:
                return jsonify({'error': 'Fluxo não encontrado'}), 404
            
            flow_data = flow_engine.active_flows[flow_id]
        elif data.get('flow_data'):
            # Testa fluxo novo
            flow_data = data['flow_data']
        else:
            return jsonify({'error': 'Dados do fluxo são obrigatórios'}), 400
        
        test_phone = data.get('test_phone', '5511999999999')
        test_message = data.get('test_message', 'teste')
        
        # Valida estrutura
        if not flow_engine._validate_flow(flow_data):
            return jsonify({'error': 'Estrutura do fluxo inválida'}), 400
        
        # Obtém handler do WhatsApp
        try:
            from web.app import whatsapp
            whatsapp_handler = whatsapp
        except:
            whatsapp_handler = None
        
        # Cria fluxo temporário para teste
        temp_flow_id = 99999
        flow_engine.load_flow(temp_flow_id, flow_data)
        
        # Executa fluxo
        result = flow_engine.execute_flow(
            flow_id=temp_flow_id,
            phone=test_phone,
            initial_message=test_message,
            whatsapp_handler=whatsapp_handler
        )
        
        # Remove fluxo temporário
        flow_engine.unload_flow(temp_flow_id)
        
        return jsonify({
            'success': True,
            'result': result
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/templates', methods=['GET'])
def get_templates():
    """Retorna templates de fluxos prontos"""
    templates = [
        {
            'name': 'Boas-vindas',
            'description': 'Fluxo de boas-vindas simples',
            'flow_data': {
                'name': 'Boas-vindas',
                'trigger': {
                    'type': 'keyword',
                    'keywords': ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite']
                },
                'steps': [
                    {
                        'type': 'send_message',
                        'message': 'Olá! 👋 Bem-vindo! Como posso ajudar você hoje?'
                    },
                    {
                        'type': 'wait',
                        'duration': 3
                    },
                    {
                        'type': 'ai_response'
                    }
                ]
            }
        },
        {
            'name': 'Atendimento com IA',
            'description': 'Responde automaticamente com IA',
            'flow_data': {
                'name': 'Atendimento com IA',
                'trigger': {
                    'type': 'always'
                },
                'steps': [
                    {
                        'type': 'ai_response'
                    }
                ]
            }
        },
        {
            'name': 'Informações de Produto',
            'description': 'Fornece informações sobre produtos',
            'flow_data': {
                'name': 'Informações de Produto',
                'trigger': {
                    'type': 'keyword',
                    'keywords': ['produto', 'preço', 'valor', 'quanto custa', 'informação']
                },
                'steps': [
                    {
                        'type': 'send_message',
                        'message': 'Vou buscar informações para você!'
                    },
                    {
                        'type': 'wait',
                        'duration': 2
                    },
                    {
                        'type': 'ai_response'
                    }
                ]
            }
        }
    ]
    
    return jsonify({
        'success': True,
        'templates': templates
    }), 200
