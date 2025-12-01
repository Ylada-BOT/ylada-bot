"""
Sistema de Campanhas com QR Code
Similar ao Botconversa - cria campanhas com links e QR Codes
"""
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
import uuid
from pathlib import Path
import qrcode
from io import BytesIO
import base64


class CampaignsManager:
    """Gerencia campanhas com QR Code e links"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.campaigns_file = self.data_dir / "campaigns.json"
        self.campaigns = self._load_campaigns()
        self.base_url = os.getenv("BASE_URL", "http://localhost:5000")
    
    def _load_campaigns(self) -> Dict:
        """Carrega campanhas do arquivo"""
        if self.campaigns_file.exists():
            try:
                with open(self.campaigns_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_campaigns(self):
        """Salva campanhas no arquivo"""
        with open(self.campaigns_file, "w", encoding="utf-8") as f:
            json.dump(self.campaigns, f, indent=2, ensure_ascii=False)
    
    def create_campaign(self, name: str, message: str, flow_name: Optional[str] = None) -> Dict:
        """
        Cria nova campanha com QR Code e link
        
        Args:
            name: Nome da campanha
            message: Mensagem inicial da campanha
            flow_name: Nome do fluxo a ser acionado (opcional)
        
        Returns:
            Dict com dados da campanha criada
        """
        campaign_id = str(uuid.uuid4())[:8]
        link = f"{self.base_url}/campaign/{campaign_id}"
        
        campaign = {
            "id": campaign_id,
            "name": name,
            "message": message,
            "flow_name": flow_name,
            "link": link,
            "qr_code": self._generate_qr_code(link),
            "created_at": datetime.now().isoformat(),
            "clicks": 0,
            "conversions": 0,
            "active": True
        }
        
        self.campaigns[campaign_id] = campaign
        self._save_campaigns()
        return campaign
    
    def _generate_qr_code(self, data: str) -> str:
        """Gera QR Code em base64"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """Obtém campanha por ID"""
        return self.campaigns.get(campaign_id)
    
    def list_campaigns(self, active_only: bool = False) -> List[Dict]:
        """Lista todas as campanhas"""
        campaigns_list = list(self.campaigns.values())
        if active_only:
            campaigns_list = [c for c in campaigns_list if c.get("active", True)]
        return campaigns_list
    
    def track_click(self, campaign_id: str):
        """Registra clique na campanha"""
        campaign = self.get_campaign(campaign_id)
        if campaign:
            campaign["clicks"] = campaign.get("clicks", 0) + 1
            self._save_campaigns()
    
    def track_conversion(self, campaign_id: str):
        """Registra conversão da campanha"""
        campaign = self.get_campaign(campaign_id)
        if campaign:
            campaign["conversions"] = campaign.get("conversions", 0) + 1
            self._save_campaigns()
    
    def deactivate_campaign(self, campaign_id: str):
        """Desativa campanha"""
        campaign = self.get_campaign(campaign_id)
        if campaign:
            campaign["active"] = False
            self._save_campaigns()

