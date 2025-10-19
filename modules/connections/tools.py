#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ferramentas para gerenciar conexões MCP ativas.
"""

import logging
from typing import Dict, Any
from datetime import datetime

from modules.base import BaseModule
from core.connection_monitor import get_connection_monitor


class ConnectionTools(BaseModule):
    """Ferramentas para monitorar conexões MCP."""
    
    def __init__(self):
        super().__init__()
        self.monitor = get_connection_monitor()
    
    async def is_available(self) -> bool:
        """Módulo sempre disponível."""
        return True
    
    async def initialize(self):
        """Inicializa o módulo."""
        self.initialized = True
        self.logger.info("Módulo de conexões inicializado")
    
    def get_tools(self) -> Dict[str, callable]:
        """Retorna as ferramentas de conexões."""
        return {
            "list_connections": self.list_connections,
            "get_connection_stats": self.get_connection_stats,
            "get_connection_details": self.get_connection_details
        }
    
    async def list_connections(
        self,
        status: str = "all"
    ) -> str:
        """
        Lista todas as conexões MCP ativas.
        
        Args:
            status: Filtrar por status (all, active, idle, disconnected)
        
        Returns:
            Lista formatada de conexões
        """
        try:
            if status == "active":
                clients = self.monitor.get_active_clients()
            elif status == "all":
                clients = self.monitor.get_all_clients()
            else:
                # Filtrar por status específico
                clients = [c for c in self.monitor.get_all_clients() if c.status == status]
            
            if not clients:
                return f"Nenhuma conexão encontrada com status: {status}"
            
            # Formatar saída
            lines = [f"🔌 Conexões MCP ({len(clients)} encontradas):\n"]
            
            for client in clients:
                status_emoji = {
                    "active": "🟢",
                    "idle": "🟡", 
                    "disconnected": "🔴"
                }.get(client.status, "⚪")
                
                lines.append(f"{status_emoji} {client.client_name}")
                lines.append(f"   ID: {client.client_id}")
                lines.append(f"   Conectado em: {self._format_datetime(client.connected_at)}")
                lines.append(f"   Última atividade: {self._format_datetime(client.last_activity)}")
                lines.append(f"   Requisições: {client.requests_count}")
                
                if client.tools_used:
                    lines.append(f"   Ferramentas usadas: {', '.join(client.tools_used[:5])}")
                    if len(client.tools_used) > 5:
                        lines.append(f"   ... e mais {len(client.tools_used) - 5}")
                
                lines.append("")
            
            return "\n".join(lines)
            
        except Exception as e:
            self.logger.error(f"Erro ao listar conexões: {e}")
            return f"❌ Erro ao listar conexões: {str(e)}"
    
    async def get_connection_stats(self) -> str:
        """
        Retorna estatísticas gerais das conexões.
        
        Returns:
            Estatísticas formatadas
        """
        try:
            stats = self.monitor.get_stats()
            
            lines = [
                "📊 Estatísticas de Conexões MCP\n",
                f"Total de clientes: {stats['total_clients']}",
                f"🟢 Ativos: {stats['active_clients']}",
                f"🟡 Inativos: {stats['idle_clients']}",
                f"🔴 Desconectados: {stats['disconnected_clients']}",
                f"\nTotal de requisições: {stats['total_requests']}",
                f"Atualizado em: {self._format_datetime(stats['timestamp'])}"
            ]
            
            return "\n".join(lines)
            
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")
            return f"❌ Erro ao obter estatísticas: {str(e)}"
    
    async def get_connection_details(
        self,
        client_id: str
    ) -> str:
        """
        Retorna detalhes de uma conexão específica.
        
        Args:
            client_id: ID do cliente
        
        Returns:
            Detalhes formatados da conexão
        """
        try:
            client = self.monitor.get_client(client_id)
            
            if not client:
                return f"❌ Cliente não encontrado: {client_id}"
            
            status_emoji = {
                "active": "🟢",
                "idle": "🟡",
                "disconnected": "🔴"
            }.get(client.status, "⚪")
            
            lines = [
                f"📋 Detalhes da Conexão\n",
                f"{status_emoji} Status: {client.status}",
                f"Nome: {client.client_name}",
                f"ID: {client.client_id}",
                f"Conectado em: {self._format_datetime(client.connected_at)}",
                f"Última atividade: {self._format_datetime(client.last_activity)}",
                f"Total de requisições: {client.requests_count}",
            ]
            
            if client.tools_used:
                lines.append(f"\n🛠️ Ferramentas utilizadas ({len(client.tools_used)}):")
                for tool in client.tools_used:
                    lines.append(f"  • {tool}")
            else:
                lines.append("\n🛠️ Nenhuma ferramenta utilizada ainda")
            
            return "\n".join(lines)
            
        except Exception as e:
            self.logger.error(f"Erro ao obter detalhes: {e}")
            return f"❌ Erro ao obter detalhes: {str(e)}"
    
    def _format_datetime(self, dt_str: str) -> str:
        """Formata uma string datetime para exibição."""
        try:
            dt = datetime.fromisoformat(dt_str)
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except:
            return dt_str
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna o status do módulo."""
        stats = self.monitor.get_stats()
        return {
            "available": True,
            "connections": stats
        }
