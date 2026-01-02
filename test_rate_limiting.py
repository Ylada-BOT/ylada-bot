#!/usr/bin/env python3
"""
Script de teste para Rate Limiting

Uso:
    python3 test_rate_limiting.py
"""
import requests
import time
import sys

def test_rate_limiting():
    """Testa rate limiting"""
    print("\n" + "="*50)
    print("🧪 TESTE DE RATE LIMITING")
    print("="*50 + "\n")
    
    base_url = "http://localhost:5002"
    endpoint = f"{base_url}/webhook"
    
    # Teste 1: Enviar 1 requisição (deve funcionar)
    print("[1/3] Teste 1: Enviar 1 requisição...")
    try:
        response = requests.post(
            endpoint,
            json={"from": "5511999999999", "body": "teste 1"},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Requisição 1: Sucesso\n")
        else:
            print(f"⚠️ Requisição 1: Status {response.status_code}\n")
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando!")
        print("   Inicie o servidor com: python3 web/app.py\n")
        return
    except Exception as e:
        print(f"❌ Erro: {e}\n")
        return
    
    # Teste 2: Enviar 20 requisições rapidamente
    print("[2/3] Teste 2: Enviar 20 requisições rapidamente...")
    print("   (Limite: 15/min, esperamos ver 429 após 15)\n")
    
    success_count = 0
    rate_limited_count = 0
    error_count = 0
    
    for i in range(1, 21):
        try:
            response = requests.post(
                endpoint,
                json={"from": "5511999999999", "body": f"teste {i}"},
                timeout=5
            )
            
            if response.status_code == 200:
                success_count += 1
                print(f"   [{i:2d}] ✅ Sucesso")
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"   [{i:2d}] ⛔ Rate Limited (429)")
            else:
                error_count += 1
                print(f"   [{i:2d}] ⚠️ Status {response.status_code}")
            
            # Pequeno delay para não sobrecarregar
            time.sleep(0.1)
            
        except Exception as e:
            error_count += 1
            print(f"   [{i:2d}] ❌ Erro: {e}")
    
    # Resultados
    print("\n" + "="*50)
    print("📊 RESULTADOS")
    print("="*50)
    print(f"✅ Sucessos: {success_count}")
    print(f"⛔ Rate Limited (429): {rate_limited_count}")
    print(f"❌ Erros: {error_count}")
    print("="*50 + "\n")
    
    # Teste 3: Aguardar e tentar novamente
    print("[3/3] Teste 3: Aguardar 60 segundos e tentar novamente...")
    print("   (Rate limit deve resetar)\n")
    
    print("   ⏳ Aguardando 10 segundos (teste rápido)...")
    time.sleep(10)
    
    try:
        response = requests.post(
            endpoint,
            json={"from": "5511999999999", "body": "teste após espera"},
            timeout=5
        )
        if response.status_code == 200:
            print("   ✅ Requisição após espera: Sucesso")
            print("   (Rate limit resetou parcialmente)\n")
        elif response.status_code == 429:
            print("   ⛔ Requisição após espera: Ainda rate limited")
            print("   (Aguarde mais tempo para reset completo)\n")
        else:
            print(f"   ⚠️ Requisição após espera: Status {response.status_code}\n")
    except Exception as e:
        print(f"   ❌ Erro: {e}\n")
    
    # Conclusão
    print("="*50)
    if rate_limited_count > 0:
        print("✅ TESTE PASSOU! Rate limiting está funcionando.")
        print(f"   {rate_limited_count} requisições foram bloqueadas corretamente.")
    elif success_count >= 15:
        print("⚠️ TESTE PARCIAL: Rate limiting pode não estar ativo.")
        print("   Verifique se flask-limiter está instalado e configurado.")
    else:
        print("❌ TESTE FALHOU: Resultados inesperados.")
    print("="*50 + "\n")

if __name__ == '__main__':
    try:
        test_rate_limiting()
    except KeyboardInterrupt:
        print("\n\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()



