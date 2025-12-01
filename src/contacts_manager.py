"""
Gerenciador de Contatos do Bot Ylada
Gerencia contatos, histórico, tags e categorias
"""
from typing import Dict, List, Optional, Set
from datetime import datetime
import json
import os


class ContactsManager:
    """Gerencia contatos e suas informações"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.contacts_file = os.path.join(data_dir, "contacts.json")
        self.contacts: Dict[str, Dict] = {}
        self._ensure_data_dir()
        self._load_contacts()
    
    def _ensure_data_dir(self):
        """Garante que o diretório de dados existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
    
    def _load_contacts(self):
        """Carrega contatos do arquivo"""
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, "r", encoding="utf-8") as f:
                    self.contacts = json.load(f)
            except Exception as e:
                print(f"[!] Erro ao carregar contatos: {e}")
                self.contacts = {}
        else:
            self.contacts = {}
    
    def _save_contacts(self):
        """Salva contatos no arquivo"""
        try:
            with open(self.contacts_file, "w", encoding="utf-8") as f:
                json.dump(self.contacts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Erro ao salvar contatos: {e}")
    
    def get_or_create_contact(self, phone: str, name: Optional[str] = None) -> Dict:
        """
        Obtém ou cria um contato
        
        Args:
            phone: Número do telefone
            name: Nome do contato (opcional)
        
        Returns:
            Dict com informações do contato
        """
        if phone not in self.contacts:
            self.contacts[phone] = {
                "phone": phone,
                "name": name or phone,
                "tags": [],
                "category": "geral",
                "notes": "",
                "created_at": datetime.now().isoformat(),
                "last_interaction": datetime.now().isoformat(),
                "interaction_count": 0,
                "message_history": []
            }
            self._save_contacts()
        else:
            # Atualiza última interação
            self.contacts[phone]["last_interaction"] = datetime.now().isoformat()
            self.contacts[phone]["interaction_count"] = self.contacts[phone].get("interaction_count", 0) + 1
            if name and name != phone:
                self.contacts[phone]["name"] = name
            self._save_contacts()
        
        return self.contacts[phone]
    
    def add_message_to_history(self, phone: str, message: str, direction: str = "received"):
        """
        Adiciona mensagem ao histórico
        
        Args:
            phone: Número do telefone
            message: Conteúdo da mensagem
            direction: "received" ou "sent"
        """
        contact = self.get_or_create_contact(phone)
        
        if "message_history" not in contact:
            contact["message_history"] = []
        
        contact["message_history"].append({
            "message": message,
            "direction": direction,
            "timestamp": datetime.now().isoformat()
        })
        
        # Mantém apenas últimas 100 mensagens
        if len(contact["message_history"]) > 100:
            contact["message_history"] = contact["message_history"][-100:]
        
        self._save_contacts()
    
    def add_tag(self, phone: str, tag: str):
        """Adiciona tag a um contato"""
        contact = self.get_or_create_contact(phone)
        if "tags" not in contact:
            contact["tags"] = []
        
        if tag not in contact["tags"]:
            contact["tags"].append(tag)
            self._save_contacts()
    
    def remove_tag(self, phone: str, tag: str):
        """Remove tag de um contato"""
        if phone in self.contacts and tag in self.contacts[phone].get("tags", []):
            self.contacts[phone]["tags"].remove(tag)
            self._save_contacts()
    
    def set_category(self, phone: str, category: str):
        """Define categoria de um contato"""
        contact = self.get_or_create_contact(phone)
        contact["category"] = category
        self._save_contacts()
    
    def set_notes(self, phone: str, notes: str):
        """Define notas sobre um contato"""
        contact = self.get_or_create_contact(phone)
        contact["notes"] = notes
        self._save_contacts()
    
    def get_contact(self, phone: str) -> Optional[Dict]:
        """Obtém informações de um contato"""
        return self.contacts.get(phone)
    
    def list_contacts(self, category: Optional[str] = None, tag: Optional[str] = None, search: Optional[str] = None) -> List[Dict]:
        """
        Lista contatos com filtros
        
        Args:
            category: Filtrar por categoria
            tag: Filtrar por tag
            search: Buscar por nome ou telefone
        
        Returns:
            Lista de contatos
        """
        results = list(self.contacts.values())
        
        if category:
            results = [c for c in results if c.get("category") == category]
        
        if tag:
            results = [c for c in results if tag in c.get("tags", [])]
        
        if search:
            search_lower = search.lower()
            results = [
                c for c in results
                if search_lower in c.get("name", "").lower() or search_lower in c.get("phone", "")
            ]
        
        # Ordena por última interação (mais recente primeiro)
        results.sort(key=lambda x: x.get("last_interaction", ""), reverse=True)
        
        return results
    
    def get_all_tags(self) -> Set[str]:
        """Retorna todas as tags usadas"""
        tags = set()
        for contact in self.contacts.values():
            tags.update(contact.get("tags", []))
        return tags
    
    def get_all_categories(self) -> Set[str]:
        """Retorna todas as categorias usadas"""
        categories = set()
        for contact in self.contacts.values():
            categories.add(contact.get("category", "geral"))
        return categories
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas dos contatos"""
        total = len(self.contacts)
        categories = {}
        tags_count = {}
        
        for contact in self.contacts.values():
            # Conta categorias
            cat = contact.get("category", "geral")
            categories[cat] = categories.get(cat, 0) + 1
            
            # Conta tags
            for tag in contact.get("tags", []):
                tags_count[tag] = tags_count.get(tag, 0) + 1
        
        total_interactions = sum(c.get("interaction_count", 0) for c in self.contacts.values())
        
        return {
            "total_contacts": total,
            "total_interactions": total_interactions,
            "categories": categories,
            "tags_count": tags_count,
            "avg_interactions_per_contact": total_interactions / total if total > 0 else 0
        }
    
    def export_contacts_csv(self, filepath: str) -> bool:
        """Exporta contatos para CSV"""
        try:
            import csv
            
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "phone", "name", "category", "tags", "interaction_count",
                    "last_interaction", "created_at", "notes"
                ])
                writer.writeheader()
                
                for contact in self.contacts.values():
                    row = {
                        "phone": contact.get("phone", ""),
                        "name": contact.get("name", ""),
                        "category": contact.get("category", ""),
                        "tags": ";".join(contact.get("tags", [])),
                        "interaction_count": contact.get("interaction_count", 0),
                        "last_interaction": contact.get("last_interaction", ""),
                        "created_at": contact.get("created_at", ""),
                        "notes": contact.get("notes", "")
                    }
                    writer.writerow(row)
            
            return True
        except Exception as e:
            print(f"[!] Erro ao exportar CSV: {e}")
            return False

