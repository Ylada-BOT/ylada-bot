"""
Lead Scoring
Calcula pontuação de qualificação de leads
"""
from typing import Dict, Any, Optional
import re
import logging

logger = logging.getLogger(__name__)


class LeadScoring:
    """Calcula score de qualificação de leads"""
    
    # Palavras-chave que indicam interesse
    INTEREST_KEYWORDS = [
        'quero', 'preciso', 'gostaria', 'tenho interesse', 'quanto custa',
        'preço', 'valor', 'comprar', 'adquirir', 'contratar', 'fazer pedido',
        'informação', 'detalhes', 'mais sobre', 'como funciona', 'quando',
        'onde', 'disponível', 'estoque', 'entrega', 'prazo'
    ]
    
    # Palavras-chave que indicam urgência
    URGENCY_KEYWORDS = [
        'urgente', 'rápido', 'hoje', 'agora', 'imediatamente', 'já',
        'preciso agora', 'com urgência', 'o quanto antes'
    ]
    
    # Palavras-chave que indicam qualificação
    QUALIFICATION_KEYWORDS = [
        'empresa', 'negócio', 'empresarial', 'corporativo', 'equipe',
        'time', 'equipe de', 'para minha empresa'
    ]
    
    def calculate_score(
        self,
        message: str,
        has_name: bool = False,
        has_email: bool = False,
        message_count: int = 1,
        source: Optional[str] = None
    ) -> float:
        """
        Calcula score de qualificação (0-100)
        
        Args:
            message: Mensagem do lead
            has_name: Se tem nome
            has_email: Se tem email
            message_count: Número de mensagens trocadas
            source: Origem do lead
        
        Returns:
            Score de 0 a 100
        """
        score = 0.0
        message_lower = message.lower()
        
        # Base score (10 pontos)
        score += 10
        
        # Dados completos (30 pontos)
        if has_name:
            score += 15
        if has_email:
            score += 15
        
        # Palavras-chave de interesse (20 pontos)
        interest_count = sum(1 for keyword in self.INTEREST_KEYWORDS if keyword in message_lower)
        score += min(interest_count * 3, 20)
        
        # Palavras-chave de urgência (15 pontos)
        urgency_count = sum(1 for keyword in self.URGENCY_KEYWORDS if keyword in message_lower)
        score += min(urgency_count * 5, 15)
        
        # Palavras-chave de qualificação (15 pontos)
        qualification_count = sum(1 for keyword in self.QUALIFICATION_KEYWORDS if keyword in message_lower)
        score += min(qualification_count * 5, 15)
        
        # Engajamento (10 pontos)
        if message_count > 1:
            score += min((message_count - 1) * 2, 10)
        
        # Origem (10 pontos)
        if source == 'flow':
            score += 10
        elif source == 'manual':
            score += 5
        
        # Limita entre 0 e 100
        score = max(0, min(100, score))
        
        return round(score, 2)
    
    def extract_email(self, text: str) -> Optional[str]:
        """
        Extrai email de um texto
        
        Args:
            text: Texto para extrair email
        
        Returns:
            Email encontrado ou None
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """
        Extrai telefone de um texto
        
        Args:
            text: Texto para extrair telefone
        
        Returns:
            Telefone encontrado ou None
        """
        # Remove caracteres não numéricos
        phone = re.sub(r'\D', '', text)
        
        # Verifica se tem pelo menos 10 dígitos
        if len(phone) >= 10:
            return phone
        
        return None
    
    def extract_name(self, text: str) -> Optional[str]:
        """
        Tenta extrair nome de um texto (heurística simples)
        
        Args:
            text: Texto para extrair nome
        
        Returns:
            Nome encontrado ou None
        """
        # Padrões comuns de apresentação
        patterns = [
            r'(?:meu nome é|eu sou|sou o|sou a|me chamo|chamo-me)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:nome|chamo)\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:aqui|aqui está|é)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Valida se parece um nome (2-4 palavras, cada uma com maiúscula)
                words = name.split()
                if 2 <= len(words) <= 4 and all(word[0].isupper() for word in words if word):
                    return name
        
        return None
    
    def is_qualified(self, score: float, threshold: float = 50.0) -> bool:
        """
        Verifica se lead está qualificado
        
        Args:
            score: Score do lead
            threshold: Limite mínimo (padrão: 50)
        
        Returns:
            True se qualificado
        """
        return score >= threshold
