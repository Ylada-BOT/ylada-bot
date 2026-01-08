"""
Configurações gerais do sistema
"""
import os
from pathlib import Path

# Carrega variáveis de ambiente do .env.local
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / '.env.local'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[✓] Carregado .env.local de {env_path}")
    else:
        # Tenta carregar .env se .env.local não existir
        env_path = Path(__file__).resolve().parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            print(f"[✓] Carregado .env de {env_path}")
except ImportError:
    print("[!] python-dotenv não instalado. Instale com: pip install python-dotenv")
except Exception as e:
    print(f"[!] Erro ao carregar .env.local: {e}")

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# Banco de dados
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/ylada_bot'
)

# Redis (opcional)
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
USE_REDIS = os.getenv('USE_REDIS', 'false').lower() == 'true'

# WhatsApp
WHATSAPP_SERVER_PORT = int(os.getenv('WHATSAPP_SERVER_PORT', 5001))
# URL do servidor WhatsApp (localhost em dev, URL externa em produção)
WHATSAPP_SERVER_URL = os.getenv('WHATSAPP_SERVER_URL', f'http://localhost:{WHATSAPP_SERVER_PORT}')
# Detecta se está em produção (Railway, Vercel, Render, etc)
IS_PRODUCTION = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('VERCEL') or os.getenv('RENDER')
if IS_PRODUCTION and not os.getenv('WHATSAPP_SERVER_URL'):
    # Em produção, assume que o servidor está na mesma URL base
    APP_URL = os.getenv('APP_URL', 'http://localhost:5002')
    WHATSAPP_SERVER_URL = APP_URL.replace(':5002', f':{WHATSAPP_SERVER_PORT}') if ':5002' in APP_URL else f'{APP_URL}:{WHATSAPP_SERVER_PORT}'
WHATSAPP_WEBHOOK_URL = os.getenv(
    'WHATSAPP_WEBHOOK_URL',
    f'http://localhost:5002/webhook'
)

# IA
AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')  # openai ou anthropic
AI_API_KEY = os.getenv('AI_API_KEY', '')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4o-mini')

# Pagamento
PAYMENT_GATEWAY = os.getenv('PAYMENT_GATEWAY', 'stripe')  # stripe, mercadopago, asaas
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN', '')
ASAAS_API_KEY = os.getenv('ASAAS_API_KEY', '')

# Aplicação
APP_NAME = 'BOT by YLADA'
APP_URL = os.getenv('APP_URL', 'http://localhost:5002')
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

# Uploads
UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Planos padrão
DEFAULT_PLANS = {
    'free': {
        'name': 'Grátis',
        'price': 0,
        'max_instances': 1,
        'max_flows': 3,
        'max_messages_month': 1000,
        'features': ['basic_ai', 'basic_flows']
    },
    'basic': {
        'name': 'Básico',
        'price': 49.90,
        'max_instances': 2,
        'max_flows': 10,
        'max_messages_month': 5000,
        'features': ['ai', 'flows', 'notifications', 'analytics']
    },
    'pro': {
        'name': 'Profissional',
        'price': 149.90,
        'max_instances': 5,
        'max_flows': 50,
        'max_messages_month': 20000,
        'features': ['ai', 'flows', 'notifications', 'analytics', 'api', 'templates']
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': 499.90,
        'max_instances': -1,  # Ilimitado
        'max_flows': -1,
        'max_messages_month': -1,
        'features': ['all', 'white_label', 'priority_support', 'custom_integrations']
    }
}
