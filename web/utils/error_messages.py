"""
Utilitário para mensagens de erro amigáveis ao usuário
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def get_friendly_error_message(error: Exception, context: str = "", operation: str = "") -> Dict[str, Any]:
    """
    Retorna mensagem de erro amigável para o usuário
    
    Args:
        error: Exceção que ocorreu
        context: Contexto adicional (ex: "ao carregar conversas")
        operation: Operação que estava sendo executada (ex: "carregar conversas")
    
    Returns:
        dict com error, message, hint, solution, details
    """
    error_str = str(error).lower()
    error_type = type(error).__name__
    
    # Erro de conexão com WhatsApp
    if 'connection' in error_str or '503' in error_str or 'ConnectionError' in error_type:
        return {
            "error": "Servidor WhatsApp não está disponível",
            "message": f"Não foi possível conectar ao servidor WhatsApp {context}.",
            "hint": "Verifique se o serviço WhatsApp está rodando no Railway.",
            "solution": "Configure WHATSAPP_SERVER_URL no Railway ou aguarde alguns segundos e tente novamente.",
            "details": str(error) if logger.level <= logging.DEBUG else None
        }
    
    # Erro de timeout
    if 'timeout' in error_str or 'Timeout' in error_type:
        return {
            "error": "Tempo de espera esgotado",
            "message": f"O servidor demorou muito para responder {context}.",
            "hint": "O servidor pode estar sobrecarregado ou lento.",
            "solution": "Tente novamente em alguns segundos. Se o problema persistir, verifique os logs do servidor.",
            "details": str(error) if logger.level <= logging.DEBUG else None
        }
    
    # Erro de autenticação
    if '401' in error_str or 'unauthorized' in error_str or 'Unauthorized' in error_type:
        return {
            "error": "Não autenticado",
            "message": "Você precisa fazer login para acessar esta funcionalidade.",
            "hint": "Sua sessão pode ter expirado.",
            "solution": "Faça login novamente.",
            "details": None
        }
    
    # Erro de permissão
    if '403' in error_str or 'forbidden' in error_str or 'Forbidden' in error_type:
        return {
            "error": "Acesso negado",
            "message": "Você não tem permissão para realizar esta ação.",
            "hint": "Verifique se você tem as permissões necessárias.",
            "solution": "Entre em contato com o administrador se precisar de acesso.",
            "details": None
        }
    
    # Erro de não encontrado
    if '404' in error_str or 'not found' in error_str or 'NotFound' in error_type:
        return {
            "error": "Recurso não encontrado",
            "message": f"O recurso solicitado não foi encontrado {context}.",
            "hint": "O recurso pode ter sido removido ou não existe.",
            "solution": "Verifique se o ID está correto ou tente recarregar a página.",
            "details": None
        }
    
    # Erro de banco de dados
    if 'database' in error_str or 'psycopg2' in error_str or 'OperationalError' in error_type:
        return {
            "error": "Erro de conexão com banco de dados",
            "message": "Não foi possível conectar ao banco de dados.",
            "hint": "Verifique se a DATABASE_URL está configurada corretamente.",
            "solution": "Verifique as configurações do banco de dados no Railway ou Supabase.",
            "details": str(error) if logger.level <= logging.DEBUG else None
        }
    
    # Erro de validação
    if 'validation' in error_str or 'invalid' in error_str or 'ValueError' in error_type:
        return {
            "error": "Dados inválidos",
            "message": f"Os dados fornecidos são inválidos {context}.",
            "hint": "Verifique se todos os campos estão preenchidos corretamente.",
            "solution": "Revise os dados e tente novamente.",
            "details": str(error) if logger.level <= logging.DEBUG else None
        }
    
    # Erro genérico
    return {
        "error": "Erro inesperado",
        "message": f"Ocorreu um erro {context}." if context else "Ocorreu um erro inesperado.",
        "hint": "Verifique os logs para mais detalhes.",
        "solution": "Tente novamente ou entre em contato com o suporte se o problema persistir.",
        "details": str(error) if logger.level <= logging.DEBUG else None
    }


def format_error_response(error: Exception, context: str = "", operation: str = "", status_code: int = 500) -> tuple:
    """
    Formata resposta de erro para API
    
    Args:
        error: Exceção que ocorreu
        context: Contexto adicional
        operation: Operação que estava sendo executada
        status_code: Código HTTP de status
    
    Returns:
        tuple (json_response, status_code)
    """
    from flask import jsonify
    
    error_info = get_friendly_error_message(error, context, operation)
    
    response = {
        "success": False,
        **error_info
    }
    
    return jsonify(response), status_code

