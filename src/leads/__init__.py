"""
Sistema de Captação de Leads
Detecta, captura e gerencia leads automaticamente
"""
from .lead_manager import LeadManager
from .lead_capture import LeadCapture
from .lead_scoring import LeadScoring

__all__ = ['LeadManager', 'LeadCapture', 'LeadScoring']
