"""
Endpoint de diagnóstico para verificar status dos servidores WhatsApp
"""
from flask import Blueprint, jsonify
import requests
import subprocess
import os

diagnostic_bp = Blueprint('diagnostic', __name__)

@diagnostic_bp.route('/api/diagnostic/whatsapp')
def diagnostic_whatsapp():
    """
    Diagnóstico completo dos servidores WhatsApp
    Verifica status de todas as portas possíveis (5001-5010)
    """
    results = {}
    
    # Verifica portas de 5001 a 5010
    for port in range(5001, 5011):
        port_info = {
            "port": port,
            "status": "unknown",
            "health": None,
            "qr_available": None,
            "process_running": False,
            "error": None
        }
        
        # Verifica se há processo rodando na porta
        try:
            if os.name == 'posix':  # Unix/Linux/macOS
                result = subprocess.run(
                    ["lsof", "-ti", f":{port}"],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=2
                )
                if result.returncode == 0 and result.stdout.strip():
                    port_info["process_running"] = True
        except:
            pass
        
        # Verifica health endpoint
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                port_info["status"] = "running"
                port_info["health"] = response.json()
        except requests.exceptions.ConnectionError:
            port_info["status"] = "not_running"
        except Exception as e:
            port_info["status"] = "error"
            port_info["error"] = str(e)
        
        # Verifica se tem QR code disponível
        if port_info["status"] == "running":
            try:
                response = requests.get(f"http://localhost:{port}/qr", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    port_info["qr_available"] = bool(data.get('qr'))
                    port_info["ready"] = data.get('ready', False)
            except:
                pass
        
        results[port] = port_info
    
    return jsonify({
        "success": True,
        "ports": results,
        "summary": {
            "total_checked": len(results),
            "running": sum(1 for p in results.values() if p["status"] == "running"),
            "not_running": sum(1 for p in results.values() if p["status"] == "not_running"),
            "errors": sum(1 for p in results.values() if p["status"] == "error")
        }
    })

