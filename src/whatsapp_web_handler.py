"""
Integração GRATUITA com WhatsApp Web usando Selenium/Playwright
100% gratuito - não precisa de API paga!
"""
from typing import Dict, Optional, List
import time
import os


class WhatsAppWebHandler:
    """
    Handler gratuito para WhatsApp Web
    
    Usa Selenium ou Playwright para automatizar o WhatsApp Web diretamente.
    Não precisa de Z-API ou outras APIs pagas!
    """
    
    def __init__(self, use_playwright: bool = True, headless: bool = False):
        """
        Inicializa o handler
        
        Args:
            use_playwright: Se True, usa Playwright (recomendado). Se False, usa Selenium
            headless: Se True, roda sem abrir navegador (melhor para servidor)
        """
        self.use_playwright = use_playwright
        self.headless = headless
        self.browser = None
        self.page = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """
        Conecta ao WhatsApp Web
        
        Você precisa escanear o QR Code uma vez.
        Depois, a sessão fica salva.
        
        Returns:
            True se conectado com sucesso
        """
        try:
            if self.use_playwright:
                return self._connect_playwright()
            else:
                return self._connect_selenium()
        except Exception as e:
            print(f"[!] Erro ao conectar: {e}")
            return False
    
    def _connect_playwright(self) -> bool:
        """Conecta usando Playwright"""
        try:
            from playwright.sync_api import sync_playwright
            
            playwright = sync_playwright().start()
            self.browser = playwright.chromium.launch(headless=self.headless)
            context = self.browser.new_context(
                user_data_dir="./whatsapp_session"  # Salva sessão aqui
            )
            self.page = context.new_page()
            
            print("[*] Abrindo WhatsApp Web...")
            self.page.goto("https://web.whatsapp.com")
            
            # Aguarda QR Code ou conexão
            print("[*] Aguardando conexão...")
            print("[*] Escaneie o QR Code se aparecer")
            
            # Aguarda até conectar (procura por elementos que aparecem quando conectado)
            max_wait = 60  # 60 segundos
            for i in range(max_wait):
                try:
                    # Verifica se está conectado (procura por elementos do chat)
                    if self.page.locator('[data-testid="chat"]').count() > 0 or \
                       self.page.locator('div[role="textbox"]').count() > 0:
                        self.is_connected = True
                        print("[✓] Conectado ao WhatsApp Web!")
                        return True
                except:
                    pass
                
                time.sleep(1)
                if i % 10 == 0:
                    print(f"[...] Aguardando... ({i}/{max_wait}s)")
            
            print("[!] Timeout ao conectar")
            return False
            
        except ImportError:
            print("[!] Playwright não instalado. Instale com: pip install playwright")
            print("[!] Depois execute: playwright install chromium")
            return False
    
    def _connect_selenium(self) -> bool:
        """Conecta usando Selenium"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--user-data-dir=./whatsapp_session')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            self.browser = webdriver.Chrome(options=options)
            self.browser.get("https://web.whatsapp.com")
            
            print("[*] Aguardando conexão...")
            print("[*] Escaneie o QR Code se aparecer")
            
            # Aguarda conexão
            try:
                WebDriverWait(self.browser, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chat"]'))
                )
                self.is_connected = True
                print("[✓] Conectado ao WhatsApp Web!")
                return True
            except:
                print("[!] Timeout ao conectar")
                return False
                
        except ImportError:
            print("[!] Selenium não instalado. Instale com: pip install selenium")
            return False
    
    def send_message(self, phone: str, message: str) -> bool:
        """
        Envia mensagem via WhatsApp Web
        
        Args:
            phone: Número do destinatário (formato: 5511999999999)
            message: Mensagem a ser enviada
        
        Returns:
            True se enviado com sucesso
        """
        if not self.is_connected:
            print("[!] Não conectado ao WhatsApp Web")
            return False
        
        try:
            if self.use_playwright:
                return self._send_playwright(phone, message)
            else:
                return self._send_selenium(phone, message)
        except Exception as e:
            print(f"[!] Erro ao enviar mensagem: {e}")
            return False
    
    def _send_playwright(self, phone: str, message: str) -> bool:
        """Envia mensagem usando Playwright"""
        # Abre chat com o número
        chat_url = f"https://web.whatsapp.com/send?phone={phone}"
        self.page.goto(chat_url)
        time.sleep(3)
        
        # Aguarda campo de mensagem aparecer
        try:
            text_box = self.page.locator('div[role="textbox"]')
            text_box.wait_for(timeout=10000)
            
            # Digita mensagem
            text_box.fill(message)
            time.sleep(1)
            
            # Envia (Enter ou botão)
            text_box.press("Enter")
            time.sleep(2)
            
            print(f"[✓] Mensagem enviada para {phone}")
            return True
        except Exception as e:
            print(f"[!] Erro: {e}")
            return False
    
    def _send_selenium(self, phone: str, message: str) -> bool:
        """Envia mensagem usando Selenium"""
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        chat_url = f"https://web.whatsapp.com/send?phone={phone}"
        self.browser.get(chat_url)
        time.sleep(3)
        
        try:
            # Aguarda campo de mensagem
            text_box = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]'))
            )
            
            # Digita e envia
            text_box.send_keys(message)
            time.sleep(1)
            text_box.send_keys(Keys.RETURN)
            time.sleep(2)
            
            print(f"[✓] Mensagem enviada para {phone}")
            return True
        except Exception as e:
            print(f"[!] Erro: {e}")
            return False
    
    def listen_messages(self, callback):
        """
        Escuta mensagens recebidas (polling)
        
        Args:
            callback: Função que será chamada quando receber mensagem
                     callback(phone: str, message: str)
        """
        if not self.is_connected:
            print("[!] Não conectado")
            return
        
        print("[*] Escutando mensagens...")
        while True:
            try:
                if self.use_playwright:
                    self._check_messages_playwright(callback)
                else:
                    self._check_messages_selenium(callback)
                time.sleep(2)  # Verifica a cada 2 segundos
            except KeyboardInterrupt:
                print("\n[*] Parando escuta...")
                break
            except Exception as e:
                print(f"[!] Erro ao escutar: {e}")
                time.sleep(5)
    
    def _check_messages_playwright(self, callback):
        """Verifica mensagens usando Playwright"""
        # Procura por novas mensagens não lidas
        unread = self.page.locator('[data-testid="icon-unread-count"]')
        if unread.count() > 0:
            # Clica no primeiro chat não lido
            unread.first.click()
            time.sleep(2)
            
            # Pega última mensagem
            messages = self.page.locator('[data-testid="msg-container"]')
            if messages.count() > 0:
                last_msg = messages.last
                text = last_msg.inner_text()
                
                # Pega número do contato (precisa ajustar seletor)
                # Por enquanto, usa um placeholder
                phone = "unknown"
                callback(phone, text)
    
    def _check_messages_selenium(self, callback):
        """Verifica mensagens usando Selenium"""
        from selenium.webdriver.common.by import By
        
        unread = self.browser.find_elements(By.CSS_SELECTOR, '[data-testid="icon-unread-count"]')
        if unread:
            unread[0].click()
            time.sleep(2)
            
            messages = self.browser.find_elements(By.CSS_SELECTOR, '[data-testid="msg-container"]')
            if messages:
                text = messages[-1].text
                phone = "unknown"
                callback(phone, text)
    
    def disconnect(self):
        """Desconecta do WhatsApp Web"""
        if self.browser:
            if self.use_playwright:
                self.browser.close()
            else:
                self.browser.quit()
            self.is_connected = False
            print("[*] Desconectado")

