#!/usr/bin/env python3
"""
Script para testar conexão entre Flask e servidor WhatsApp
"""
import requests
import sys

def test_connection():
    print("🔍 Testando conexão Flask → Servidor WhatsApp")
    print("=" * 50)
    
    # Testa health
    print("\n1️⃣ Testando /health...")
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        if response.status_code == 200:
            print("   ✅ Servidor está respondendo!")
        else:
            print("   ❌ Servidor retornou erro")
    except requests.exceptions.ConnectionError:
        print("   ❌ Erro: Não conseguiu conectar ao servidor")
        print("   💡 Verifique se o servidor está rodando: ps aux | grep whatsapp_server")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Testa QR Code
    print("\n2️⃣ Testando /qr?user_id=1...")
    try:
        response = requests.get("http://localhost:5001/qr?user_id=1", timeout=30)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Ready: {data.get('ready', 'N/A')}")
        print(f"   Has QR: {data.get('hasQr', 'N/A')}")
        if data.get('qr'):
            print(f"   ✅ QR Code gerado! (tamanho: {len(data['qr'])} caracteres)")
        else:
            print(f"   ⚠️  QR Code ainda não foi gerado")
            if data.get('message'):
                print(f"   Mensagem: {data['message']}")
        if response.status_code == 200:
            print("   ✅ Endpoint /qr está funcionando!")
        else:
            print("   ❌ Endpoint retornou erro")
    except requests.exceptions.Timeout:
        print("   ❌ Timeout: Servidor demorou mais de 30 segundos")
        print("   💡 Servidor pode estar lento ou travado")
        return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Erro: Não conseguiu conectar ao servidor")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Teste concluído!")
    print("\n💡 Se ambos os testes passaram, o problema pode ser:")
    print("   1. Flask não está usando a URL correta")
    print("   2. Problema de timeout no Flask")
    print("   3. Problema de importação no Flask")
    print("\n💡 Tente recarregar a página do QR Code (F5)")
    
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

