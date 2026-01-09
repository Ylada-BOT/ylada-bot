"""
Rotas para configuração do WhatsApp (logo, perfil, etc)
"""
from flask import Blueprint, request, jsonify, send_file, send_from_directory
from pathlib import Path
import os

bp = Blueprint('whatsapp_config', __name__, url_prefix='/api/whatsapp-config')


@bp.route('/logo/prepare', methods=['GET'])
def prepare_logo():
    """
    Prepara e retorna o logo otimizado para WhatsApp (640x640)
    """
    try:
        base_dir = Path(__file__).resolve().parent.parent.parent
        logo_path = base_dir / 'web' / 'static' / 'assets' / 'logo.png'
        logo_transparent = base_dir / 'web' / 'static' / 'assets' / 'logo_transparent.png'
        
        # Tenta usar logo transparente primeiro, senão usa o normal
        if logo_transparent.exists():
            logo_file = logo_transparent
        elif logo_path.exists():
            logo_file = logo_path
        else:
            return jsonify({
                'error': 'Logo não encontrado',
                'hint': 'Adicione o logo em web/static/assets/logo.png'
            }), 404
        
        # Retorna o arquivo
        return send_file(
            str(logo_file),
            mimetype='image/png',
            as_attachment=True,
            download_name='ylada-bot-logo-whatsapp.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/logo/info', methods=['GET'])
def logo_info():
    """
    Retorna informações sobre o logo e instruções
    """
    try:
        base_dir = Path(__file__).resolve().parent.parent.parent
        logo_path = base_dir / 'web' / 'static' / 'assets' / 'logo.png'
        logo_transparent = base_dir / 'web' / 'static' / 'assets' / 'logo_transparent.png'
        
        logo_exists = logo_path.exists() or logo_transparent.exists()
        
        return jsonify({
            'logo_exists': logo_exists,
            'logo_path': str(logo_path) if logo_path.exists() else None,
            'logo_transparent_path': str(logo_transparent) if logo_transparent.exists() else None,
            'download_url': '/api/whatsapp-config/logo/prepare',
            'instructions': {
                'step1': 'Baixe o logo usando o link acima',
                'step2': 'Abra o WhatsApp no celular (mesmo número conectado)',
                'step3': 'Vá em: Configurações > Perfil',
                'step4': 'Toque na foto de perfil',
                'step5': 'Escolha o logo baixado',
                'step6': 'Salve e pronto!'
            },
            'note': 'A foto de perfil que aparece nas mensagens é a do número de telefone conectado. Configure no WhatsApp do celular.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

