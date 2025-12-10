"""
Camada de abstração do banco de dados
Suporta PostgreSQL (Supabase) ou SQLite (desenvolvimento)
"""
import os
from typing import Dict, List, Optional
from pathlib import Path
import json
import sqlite3
from datetime import datetime

# Tenta importar psycopg2 (PostgreSQL), se não tiver usa SQLite
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False
    print("[*] psycopg2 não instalado. Usando SQLite para desenvolvimento.")


class Database:
    """Camada de abstração do banco de dados"""
    
    def __init__(self, use_sqlite: bool = False):
        """
        Inicializa conexão com banco
        
        Args:
            use_sqlite: Se True, usa SQLite mesmo se PostgreSQL estiver disponível
        """
        self.use_sqlite = use_sqlite or not HAS_POSTGRES
        self.conn = None
        
        if self.use_sqlite:
            self._init_sqlite()
        else:
            self._init_postgres()
    
    def _init_postgres(self):
        """Inicializa conexão PostgreSQL (Supabase)"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'ylada_bot'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', ''),
                port=os.getenv('DB_PORT', '5432')
            )
            print("[✓] Conectado ao PostgreSQL")
        except Exception as e:
            print(f"[!] Erro ao conectar PostgreSQL: {e}")
            print("[*] Usando SQLite como fallback")
            self.use_sqlite = True
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Inicializa SQLite (desenvolvimento)"""
        db_path = Path("data/ylada_bot.db")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables_sqlite()
        print("[✓] Usando SQLite (desenvolvimento)")
    
    def _create_tables_sqlite(self):
        """Cria tabelas no SQLite"""
        cur = self.conn.cursor()
        
        # Tabela accounts
        cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                plan TEXT DEFAULT 'owner',
                status TEXT DEFAULT 'active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela instances
        cur.execute("""
            CREATE TABLE IF NOT EXISTS instances (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                instance_name TEXT NOT NULL,
                port INTEGER UNIQUE NOT NULL,
                status TEXT DEFAULT 'disconnected',
                qr_code TEXT,
                last_connected TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
                UNIQUE(account_id, instance_name)
            )
        """)
        
        # Tabela contacts
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                phone TEXT NOT NULL,
                name TEXT,
                tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
                UNIQUE(account_id, phone)
            )
        """)
        
        # Tabela conversations
        cur.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                contact_id TEXT,
                message TEXT NOT NULL,
                from_me INTEGER DEFAULT 0,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
                FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE SET NULL
            )
        """)
        
        # Tabela campaigns
        cur.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                name TEXT NOT NULL,
                message TEXT,
                qr_code_url TEXT,
                link TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
            )
        """)
        
        # Índices
        cur.execute("CREATE INDEX IF NOT EXISTS idx_contacts_account ON contacts(account_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_conversations_account ON conversations(account_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_campaigns_account ON campaigns(account_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_instances_account ON instances(account_id)")
        
        self.conn.commit()
    
    # ========== ACCOUNTS ==========
    
    def create_account(self, account_data: Dict) -> Dict:
        """Cria nova conta"""
        account_id = account_data.get('id') or self._generate_id()
        account_data['id'] = account_id
        
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO accounts (id, name, phone, plan, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                account_data['id'],
                account_data['name'],
                account_data['phone'],
                account_data.get('plan', 'owner'),
                account_data.get('status', 'active')
            ))
            self.conn.commit()
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                INSERT INTO accounts (id, name, phone, plan, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                account_data['id'],
                account_data['name'],
                account_data['phone'],
                account_data.get('plan', 'owner'),
                account_data.get('status', 'active')
            ))
            self.conn.commit()
        
        return account_data
    
    def get_account(self, account_id: str) -> Optional[Dict]:
        """Retorna conta por ID"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
            row = cur.fetchone()
            return dict(row) if row else None
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def get_account_by_phone(self, phone: str) -> Optional[Dict]:
        """Retorna conta por telefone"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM accounts WHERE phone = ?", (phone,))
            row = cur.fetchone()
            return dict(row) if row else None
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM accounts WHERE phone = %s", (phone,))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def get_all_accounts(self) -> List[Dict]:
        """Retorna todas as contas"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM accounts ORDER BY created_at")
            return [dict(row) for row in cur.fetchall()]
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM accounts ORDER BY created_at")
            return [dict(row) for row in cur.fetchall()]
    
    # ========== INSTANCES ==========
    
    def create_instance(self, instance_data: Dict) -> Dict:
        """Cria nova instância"""
        instance_id = instance_data.get('id') or self._generate_id()
        instance_data['id'] = instance_id
        
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO instances (id, account_id, instance_name, port, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                instance_data['id'],
                instance_data['account_id'],
                instance_data['instance_name'],
                instance_data['port'],
                instance_data.get('status', 'disconnected')
            ))
            self.conn.commit()
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                INSERT INTO instances (id, account_id, instance_name, port, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                instance_data['id'],
                instance_data['account_id'],
                instance_data['instance_name'],
                instance_data['port'],
                instance_data.get('status', 'disconnected')
            ))
            self.conn.commit()
        
        return instance_data
    
    def get_instance(self, instance_id: str) -> Optional[Dict]:
        """Retorna instância por ID"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM instances WHERE id = ?", (instance_id,))
            row = cur.fetchone()
            return dict(row) if row else None
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM instances WHERE id = %s", (instance_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def get_instance_by_account(self, account_id: str) -> Optional[Dict]:
        """Retorna instância da conta"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM instances WHERE account_id = ? LIMIT 1", (account_id,))
            row = cur.fetchone()
            return dict(row) if row else None
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM instances WHERE account_id = %s LIMIT 1", (account_id,))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def get_all_instances(self) -> List[Dict]:
        """Retorna todas as instâncias"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM instances ORDER BY port")
            return [dict(row) for row in cur.fetchall()]
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM instances ORDER BY port")
            return [dict(row) for row in cur.fetchall()]
    
    def update_instance_status(self, instance_id: str, status: str, qr_code: Optional[str] = None):
        """Atualiza status da instância"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            if qr_code:
                cur.execute("""
                    UPDATE instances 
                    SET status = ?, qr_code = ?, last_connected = ?
                    WHERE id = ?
                """, (status, qr_code, datetime.now().isoformat() if status == 'connected' else None, instance_id))
            else:
                cur.execute("""
                    UPDATE instances 
                    SET status = ?, last_connected = ?
                    WHERE id = ?
                """, (status, datetime.now().isoformat() if status == 'connected' else None, instance_id))
            self.conn.commit()
        else:
            cur = self.conn.cursor()
            if qr_code:
                cur.execute("""
                    UPDATE instances 
                    SET status = %s, qr_code = %s, last_connected = %s
                    WHERE id = %s
                """, (status, qr_code, datetime.now() if status == 'connected' else None, instance_id))
            else:
                cur.execute("""
                    UPDATE instances 
                    SET status = %s, last_connected = %s
                    WHERE id = %s
                """, (status, datetime.now() if status == 'connected' else None, instance_id))
            self.conn.commit()
    
    # ========== CONTACTS ==========
    
    def create_contact(self, contact_data: Dict) -> Dict:
        """Cria novo contato"""
        contact_id = contact_data.get('id') or self._generate_id()
        contact_data['id'] = contact_id
        
        tags_str = json.dumps(contact_data.get('tags', [])) if isinstance(contact_data.get('tags'), list) else contact_data.get('tags', '[]')
        
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO contacts (id, account_id, phone, name, tags)
                VALUES (?, ?, ?, ?, ?)
            """, (
                contact_id,
                contact_data['account_id'],
                contact_data['phone'],
                contact_data.get('name'),
                tags_str
            ))
            self.conn.commit()
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                INSERT INTO contacts (id, account_id, phone, name, tags)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (account_id, phone) DO UPDATE
                SET name = EXCLUDED.name, tags = EXCLUDED.tags
            """, (
                contact_id,
                contact_data['account_id'],
                contact_data['phone'],
                contact_data.get('name'),
                tags_str
            ))
            self.conn.commit()
        
        contact_data['id'] = contact_id
        return contact_data
    
    def get_contacts_by_account(self, account_id: str) -> List[Dict]:
        """Retorna contatos da conta (isolado)"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM contacts WHERE account_id = ? ORDER BY created_at DESC", (account_id,))
            rows = cur.fetchall()
            contacts = []
            for row in rows:
                contact = dict(row)
                # Parse tags
                try:
                    contact['tags'] = json.loads(contact.get('tags', '[]'))
                except:
                    contact['tags'] = []
                contacts.append(contact)
            return contacts
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM contacts WHERE account_id = %s ORDER BY created_at DESC", (account_id,))
            return [dict(row) for row in cur.fetchall()]
    
    def get_contact_by_phone(self, account_id: str, phone: str) -> Optional[Dict]:
        """Retorna contato por telefone"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM contacts WHERE account_id = ? AND phone = ?", (account_id, phone))
            row = cur.fetchone()
            if row:
                contact = dict(row)
                try:
                    contact['tags'] = json.loads(contact.get('tags', '[]'))
                except:
                    contact['tags'] = []
                return contact
            return None
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM contacts WHERE account_id = %s AND phone = %s", (account_id, phone))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def update_contact(self, contact_id: str, updates: Dict):
        """Atualiza contato"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            if 'name' in updates:
                cur.execute("UPDATE contacts SET name = ? WHERE id = ?", (updates['name'], contact_id))
            if 'tags' in updates:
                tags_str = json.dumps(updates['tags']) if isinstance(updates['tags'], list) else updates['tags']
                cur.execute("UPDATE contacts SET tags = ? WHERE id = ?", (tags_str, contact_id))
            self.conn.commit()
        else:
            cur = self.conn.cursor()
            if 'name' in updates:
                cur.execute("UPDATE contacts SET name = %s WHERE id = %s", (updates['name'], contact_id))
            if 'tags' in updates:
                tags_str = json.dumps(updates['tags']) if isinstance(updates['tags'], list) else updates['tags']
                cur.execute("UPDATE contacts SET tags = %s WHERE id = %s", (tags_str, contact_id))
            self.conn.commit()
    
    # ========== CONVERSATIONS ==========
    
    def create_conversation(self, conversation_data: Dict) -> Dict:
        """Cria nova conversa/mensagem"""
        conversation_id = conversation_data.get('id') or self._generate_id()
        conversation_data['id'] = conversation_id
        
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO conversations (id, account_id, contact_id, message, from_me)
                VALUES (?, ?, ?, ?, ?)
            """, (
                conversation_id,
                conversation_data['account_id'],
                conversation_data.get('contact_id'),
                conversation_data['message'],
                1 if conversation_data.get('from_me', False) else 0
            ))
            self.conn.commit()
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                INSERT INTO conversations (id, account_id, contact_id, message, from_me)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                conversation_id,
                conversation_data['account_id'],
                conversation_data.get('contact_id'),
                conversation_data['message'],
                conversation_data.get('from_me', False)
            ))
            self.conn.commit()
        
        conversation_data['id'] = conversation_id
        return conversation_data
    
    def get_conversations_by_account(self, account_id: str, limit: int = 100) -> List[Dict]:
        """Retorna conversas da conta (isolado)"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT * FROM conversations 
                WHERE account_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (account_id, limit))
            return [dict(row) for row in cur.fetchall()]
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT * FROM conversations 
                WHERE account_id = %s 
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (account_id, limit))
            return [dict(row) for row in cur.fetchall()]
    
    # ========== CAMPAIGNS ==========
    
    def create_campaign(self, campaign_data: Dict) -> Dict:
        """Cria nova campanha"""
        campaign_id = campaign_data.get('id') or self._generate_id()
        campaign_data['id'] = campaign_id
        
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO campaigns (id, account_id, name, message, qr_code_url, link)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                campaign_id,
                campaign_data['account_id'],
                campaign_data['name'],
                campaign_data.get('message'),
                campaign_data.get('qr_code_url'),
                campaign_data.get('link')
            ))
            self.conn.commit()
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                INSERT INTO campaigns (id, account_id, name, message, qr_code_url, link)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                campaign_id,
                campaign_data['account_id'],
                campaign_data['name'],
                campaign_data.get('message'),
                campaign_data.get('qr_code_url'),
                campaign_data.get('link')
            ))
            self.conn.commit()
        
        campaign_data['id'] = campaign_id
        return campaign_data
    
    def get_campaigns_by_account(self, account_id: str) -> List[Dict]:
        """Retorna campanhas da conta (isolado)"""
        if self.use_sqlite:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM campaigns WHERE account_id = ? ORDER BY created_at DESC", (account_id,))
            return [dict(row) for row in cur.fetchall()]
        else:
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM campaigns WHERE account_id = %s ORDER BY created_at DESC", (account_id,))
            return [dict(row) for row in cur.fetchall()]
    
    # ========== UTILS ==========
    
    def _generate_id(self) -> str:
        """Gera ID único"""
        import uuid
        return str(uuid.uuid4())
    
    def close(self):
        """Fecha conexão"""
        if self.conn:
            self.conn.close()

