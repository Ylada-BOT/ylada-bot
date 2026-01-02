#!/usr/bin/env python3
"""
Script de teste para Fila de Mensagens

Uso:
    python3 test_queue.py
"""
import sys
import os
import time

# Adiciona paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

from web.utils.message_queue import init_message_queue, get_message_queue
from web.workers.message_worker import init_message_worker

def test_queue():
    """Testa fila de mensagens"""
    print("\n" + "="*50)
    print("🧪 TESTE DE FILA DE MENSAGENS")
    print("="*50 + "\n")
    
    # Inicializa fila
    print("[1/5] Inicializando fila...")
    queue = init_message_queue(use_redis=False)
    print(f"✅ Fila inicializada. Tamanho: {queue.get_queue_size()}\n")
    
    # Adiciona mensagens
    print("[2/5] Adicionando mensagens à fila...")
    message_ids = []
    for i in range(3):
        message_id = queue.add_message(
            phone=f"551199999{i:04d}",
            message=f"Mensagem de teste {i+1}",
            priority=i,
            max_retries=3,
            retry_delay=2
        )
        message_ids.append(message_id)
        print(f"   ✅ Mensagem {i+1} adicionada: {message_id}")
    
    print(f"\n📊 Tamanho da fila: {queue.get_queue_size()}\n")
    
    # Verifica se WhatsApp está disponível
    print("[3/5] Verificando WhatsApp...")
    try:
        from web.app import whatsapp
        
        if whatsapp and whatsapp.is_ready():
            print("✅ WhatsApp está conectado\n")
            
            # Inicia worker
            print("[4/5] Iniciando worker...")
            worker = init_message_worker(queue, whatsapp, interval=1.0)
            print("✅ Worker iniciado\n")
            
            # Processa mensagens
            print("[5/5] Processando mensagens (aguarde 10 segundos)...")
            print("   ⏳ Worker processando em background...\n")
            
            for i in range(10):
                time.sleep(1)
                stats = worker.get_stats()
                queue_size = queue.get_queue_size()
                print(f"   [{i+1}/10] Processadas: {stats['processed']} | Falhadas: {stats['failed']} | Fila: {queue_size}")
            
            # Estatísticas finais
            print("\n" + "="*50)
            print("📊 ESTATÍSTICAS FINAIS")
            print("="*50)
            final_stats = worker.get_stats()
            print(f"✅ Processadas: {final_stats['processed']}")
            print(f"❌ Falhadas: {final_stats['failed']}")
            print(f"📋 Fila: {final_stats['queue_size']}")
            print(f"🔄 Processando: {final_stats['processing']}")
            print("="*50 + "\n")
            
            if final_stats['processed'] > 0:
                print("✅ TESTE PASSOU! Mensagens foram processadas.")
            else:
                print("⚠️ TESTE PARCIAL: Nenhuma mensagem foi processada.")
                print("   Verifique se WhatsApp está realmente conectado.")
        else:
            print("⚠️ WhatsApp não está conectado.")
            print("   Conecte primeiro em: http://localhost:5002/qr")
            print("\n📋 Mensagens foram adicionadas à fila e serão processadas")
            print("   quando WhatsApp estiver conectado.\n")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\n⚠️ Não foi possível testar envio, mas a fila está funcionando.")
        print("   Mensagens foram adicionadas e serão processadas quando")
        print("   WhatsApp estiver disponível.\n")

if __name__ == '__main__':
    try:
        test_queue()
    except KeyboardInterrupt:
        print("\n\n⏹️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()



