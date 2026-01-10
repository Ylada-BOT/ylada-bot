"""
Utilitário para requisições HTTP com retry automático e backoff exponencial
"""
import requests
import time
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def retry_request(
    method: str,
    url: str,
    max_retries: int = 3,
    timeout: int = 15,
    retry_delay: int = 2,
    **kwargs
) -> requests.Response:
    """
    Faz requisição HTTP com retry automático e backoff exponencial
    
    Args:
        method: Método HTTP (get, post, put, delete, etc)
        url: URL da requisição
        max_retries: Número máximo de tentativas (padrão: 3)
        timeout: Timeout em segundos (padrão: 15)
        retry_delay: Delay inicial entre tentativas em segundos (padrão: 2)
        **kwargs: Argumentos adicionais para requests (json, headers, params, etc)
    
    Returns:
        Response object
    
    Raises:
        requests.RequestException: Se todas as tentativas falharem
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Tentativa {attempt + 1}/{max_retries}: {method.upper()} {url}")
            
            response = requests.request(
                method=method.upper(),
                url=url,
                timeout=timeout,
                **kwargs
            )
            
            # Se status code é 2xx, retorna imediatamente
            if 200 <= response.status_code < 300:
                logger.debug(f"✓ Sucesso: {response.status_code}")
                return response
            
            # Se é 4xx (erro do cliente), não tenta novamente
            elif 400 <= response.status_code < 500:
                logger.warning(f"Erro do cliente {response.status_code}: {url}")
                return response
            
            # Se é 5xx (erro do servidor), tenta novamente
            else:
                logger.warning(f"Erro do servidor {response.status_code}: {url}")
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)  # Backoff exponencial
                    logger.info(f"Aguardando {wait_time}s antes de tentar novamente...")
                    time.sleep(wait_time)
                    continue
                return response
                
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            last_exception = e
            logger.warning(f"Erro de conexão/timeout na tentativa {attempt + 1}/{max_retries}: {str(e)}")
            
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Backoff exponencial
                logger.info(f"Aguardando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)
                continue
            
            # Última tentativa falhou
            logger.error(f"Todas as {max_retries} tentativas falharam para {url}")
            raise
            
        except requests.exceptions.RequestException as e:
            # Outros erros de requisição - não tenta novamente
            logger.error(f"Erro de requisição: {str(e)}")
            raise
    
    # Se chegou aqui, todas as tentativas falharam
    if last_exception:
        raise last_exception
    raise requests.exceptions.RequestException(f"Todas as {max_retries} tentativas falharam para {url}")


def get_with_retry(url: str, timeout: int = 15, **kwargs) -> requests.Response:
    """Conveniência para GET com retry"""
    return retry_request('get', url, timeout=timeout, **kwargs)


def post_with_retry(url: str, timeout: int = 15, **kwargs) -> requests.Response:
    """Conveniência para POST com retry"""
    return retry_request('post', url, timeout=timeout, **kwargs)

