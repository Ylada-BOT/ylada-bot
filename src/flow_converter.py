"""
Conversor de Fluxos Visuais para YAML
Converte fluxos criados no construtor visual para o formato do config.yaml
"""
from typing import Dict, List, Any
import yaml
from pathlib import Path


class FlowConverter:
    """Converte fluxos visuais para formato YAML"""
    
    @staticmethod
    def visual_to_yaml(flow_data: Dict) -> Dict:
        """
        Converte fluxo visual para formato YAML do config
        
        Args:
            flow_data: Dados do fluxo visual (nodes, connections, etc)
        
        Returns:
            Dict no formato do conversation_flows do config.yaml
        """
        flow_name = flow_data.get("name", "unnamed").lower().replace(" ", "_")
        nodes = flow_data.get("nodes", [])
        
        # Encontra nó inicial (geralmente o primeiro ou sem conexões de entrada)
        start_node = nodes[0] if nodes else None
        if not start_node:
            return {}
        
        # Constrói fluxo YAML
        yaml_flow = {
            "trigger_keywords": [],
            "welcome_message": "",
            "exit_keywords": ["sair", "voltar", "menu"],
            "exit_message": "Ok, voltando ao menu principal!",
            "steps": []
        }
        
        # Processa nós em ordem
        current_node = start_node
        step_index = 0
        
        while current_node:
            step = FlowConverter._node_to_step(current_node, step_index)
            if step:
                yaml_flow["steps"].append(step)
                step_index += 1
            
            # Encontra próximo nó (por enquanto, processa em ordem)
            # TODO: Implementar lógica de conexões quando adicionar linhas de conexão
            node_index = nodes.index(current_node) if current_node in nodes else -1
            if node_index >= 0 and node_index < len(nodes) - 1:
                current_node = nodes[node_index + 1]
            else:
                break
        
        # Adiciona mensagem final
        yaml_flow["end_message"] = "Fluxo concluído! Obrigado! 😊"
        
        return yaml_flow
    
    @staticmethod
    def _node_to_step(node: Dict, step_index: int) -> Dict:
        """Converte um nó visual em um passo YAML"""
        node_type = node.get("type")
        node_data = node.get("data", {})
        
        if node_type == "message":
            return {
                "type": "message",
                "message": node_data.get("text", "")
            }
        
        elif node_type == "question":
            return {
                "type": "question",
                "question": node_data.get("question", ""),
                "save_as": node_data.get("save_as", f"resposta_{step_index}"),
                "expected_responses": [
                    {
                        "keyword": "",
                        "response": "Obrigado pela resposta!",
                        "next_step": step_index + 1
                    }
                ],
                "error_message": "Por favor, responda a pergunta."
            }
        
        elif node_type == "keyword":
            # Palavras-chave são adicionadas ao trigger_keywords do fluxo
            # Retorna None pois será processado separadamente
            return None
        
        elif node_type == "condition":
            return {
                "type": "condition",
                "condition": node_data.get("condition", ""),
                "if_true": node_data.get("if_true", ""),
                "if_false": node_data.get("if_false", "")
            }
        
        elif node_type == "delay":
            return {
                "type": "delay",
                "seconds": node_data.get("seconds", 5)
            }
        
        else:
            # Tipos não suportados ainda
            return None
    
    @staticmethod
    def save_to_config(flow_name: str, yaml_flow: Dict, config_path: str = "config/config.yaml"):
        """
        Salva fluxo YAML no arquivo de configuração
        
        Args:
            flow_name: Nome do fluxo
            yaml_flow: Fluxo em formato YAML
            config_path: Caminho do arquivo de configuração
        """
        config_file = Path(config_path)
        
        # Carrega config existente
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}
        
        # Adiciona fluxo
        if "conversation_flows" not in config:
            config["conversation_flows"] = {}
        
        config["conversation_flows"][flow_name] = yaml_flow
        
        # Salva config
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    @staticmethod
    def import_flow(flow_file_path: str, config_path: str = "config/config.yaml"):
        """
        Importa fluxo visual e adiciona ao config.yaml
        
        Args:
            flow_file_path: Caminho do arquivo JSON do fluxo visual
            config_path: Caminho do arquivo de configuração
        """
        import json
        
        # Carrega fluxo visual
        with open(flow_file_path, "r", encoding="utf-8") as f:
            flow_data = json.load(f)
        
        # Converte para YAML
        yaml_flow = FlowConverter.visual_to_yaml(flow_data)
        
        # Salva no config
        flow_name = flow_data.get("name", "unnamed").lower().replace(" ", "_")
        FlowConverter.save_to_config(flow_name, yaml_flow, config_path)
        
        return flow_name, yaml_flow

