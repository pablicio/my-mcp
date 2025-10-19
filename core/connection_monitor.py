#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Monitoramento de Conexões MCP
Rastreia clientes conectados ao servidor (como Claude Desktop)
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class MCPClient:
    """Representa um cliente MCP conectado"""
    client_id: str
    client_name: str
    connected_at: str
    last_activity: str
    requests_count: int = 0
    tools_used: List[str] = None
    status: str = "active"  # active, idle, disconnected
    
    def __post_init__(self):
        if self.tools_used is None:
            self.tools_used = []
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return asdict(self)


class MCPConnectionMonitor:
    """Monitora conexões de clientes MCP"""
    
    def __init__(self, data_dir: Path = None):
        self.logger = logging.getLogger(__name__)
        self.clients: Dict[str, MCPClient] = {}
        self.data_dir = data_dir or Path('./data')
        self.data_dir.mkdir(exist_ok=True)
        self.connections_file = self.data_dir / 'mcp_connections.json'
        
        # Carregar conexões salvas
        self.load_connections()
    
    def register_client(self, client_id: str, client_name: str = "Unknown Client") -> MCPClient:
        """Registra um novo cliente"""
        if client_id in self.clients:
            # Cliente já existe, apenas atualizar status
            self.clients[client_id].status = "active"
            self.clients[client_id].last_activity = datetime.now().isoformat()
            self.logger.info(f"Cliente reconectado: {client_name} ({client_id})")
        else:
            # Novo cliente
            client = MCPClient(
                client_id=client_id,
                client_name=client_name,
                connected_at=datetime.now().isoformat(),
                last_activity=datetime.now().isoformat(),
                status="active"
            )
            self.clients[client_id] = client
            self.logger.info(f"Novo cliente conectado: {client_name} ({client_id})")
        
        self.save_connections()
        return self.clients[client_id]
    
    def record_activity(self, client_id: str, tool_name: str = None):
        """Registra atividade de um cliente"""
        if client_id not in self.clients:
            self.logger.warning(f"Cliente não registrado: {client_id}")
            return
        
        client = self.clients[client_id]
        client.last_activity = datetime.now().isoformat()
        client.requests_count += 1
        client.status = "active"
        
        if tool_name and tool_name not in client.tools_used:
            client.tools_used.append(tool_name)
        
        self.save_connections()
    
    def disconnect_client(self, client_id: str):
        """Marca cliente como desconectado"""
        if client_id in self.clients:
            self.clients[client_id].status = "disconnected"
            self.clients[client_id].last_activity = datetime.now().isoformat()
            self.logger.info(f"Cliente desconectado: {client_id}")
            self.save_connections()
    
    def get_active_clients(self) -> List[MCPClient]:
        """Retorna lista de clientes ativos"""
        return [c for c in self.clients.values() if c.status == "active"]
    
    def get_all_clients(self) -> List[MCPClient]:
        """Retorna todos os clientes"""
        return list(self.clients.values())
    
    def get_client(self, client_id: str) -> Optional[MCPClient]:
        """Retorna um cliente específico"""
        return self.clients.get(client_id)
    
    def get_stats(self) -> dict:
        """Retorna estatísticas de conexões"""
        active = len([c for c in self.clients.values() if c.status == "active"])
        idle = len([c for c in self.clients.values() if c.status == "idle"])
        disconnected = len([c for c in self.clients.values() if c.status == "disconnected"])
        total_requests = sum(c.requests_count for c in self.clients.values())
        
        return {
            "total_clients": len(self.clients),
            "active_clients": active,
            "idle_clients": idle,
            "disconnected_clients": disconnected,
            "total_requests": total_requests,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_connections(self):
        """Salva conexões em arquivo"""
        try:
            data = {
                "clients": {cid: c.to_dict() for cid, c in self.clients.items()},
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.connections_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Erro ao salvar conexões: {e}")
    
    def load_connections(self):
        """Carrega conexões salvas"""
        try:
            if self.connections_file.exists():
                with open(self.connections_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    for client_id, client_data in data.get("clients", {}).items():
                        self.clients[client_id] = MCPClient(**client_data)
                
                self.logger.info(f"Carregadas {len(self.clients)} conexões anteriores")
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar conexões: {e}")
    
    def cleanup_old_connections(self, days: int = 7):
        """Remove conexões antigas desconectadas"""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        removed = 0
        
        for client_id in list(self.clients.keys()):
            client = self.clients[client_id]
            if client.status == "disconnected":
                last_activity = datetime.fromisoformat(client.last_activity)
                if last_activity < cutoff:
                    del self.clients[client_id]
                    removed += 1
        
        if removed > 0:
            self.logger.info(f"Removidas {removed} conexões antigas")
            self.save_connections()


# Instância global
_monitor_instance = None

def get_connection_monitor() -> MCPConnectionMonitor:
    """Retorna instância global do monitor"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = MCPConnectionMonitor()
    return _monitor_instance
