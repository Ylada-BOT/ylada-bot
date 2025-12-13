"""
Conexão com banco de dados
Re-exporta do config para facilitar imports
"""
from config.database import (
    engine,
    SessionLocal,
    Base,
    get_db,
    init_db
)

__all__ = ['engine', 'SessionLocal', 'Base', 'get_db', 'init_db']
