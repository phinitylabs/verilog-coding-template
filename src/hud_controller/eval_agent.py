"""Eval-time Claude agent tweaks for the verilog template."""

from __future__ import annotations

import stat
from typing import Any

from asyncssh.sftp import SFTPFailure
from hud.agents.claude import ClaudeAgent
from hud.agents.claude.tools.coding import ClaudeBashTool, ClaudeTextEditorTool
from hud.agents.claude.tools.computer import ClaudeComputerTool
from hud.agents.claude.tools.mcp_proxy import ClaudeMCPProxyTool
from hud.types import MCPToolResult


class _VerilogTextEditorTool(ClaudeTextEditorTool):
    """Claude text editor where ``view`` on a directory returns a listing."""

    async def execute(self, arguments: dict[str, Any]) -> MCPToolResult:
        if arguments.get("command") == "view" and isinstance(arguments.get("path"), str):
            return await self._view(arguments["path"])
        return await super().execute(arguments)

    async def _view(self, path: str) -> MCPToolResult:
        try:
            async with self.client.conn.start_sftp_client() as sftp:
                attrs = await sftp.stat(path)
                if attrs.permissions is not None and stat.S_ISDIR(attrs.permissions):
                    return await self.file_list(path)
        except Exception:
            pass
        try:
            return await self.file_read(path)
        except SFTPFailure as exc:
            if "directory" in str(exc).lower():
                return await self.file_list(path)
            raise


class VerilogClaudeAgent(ClaudeAgent):
    """Claude agent with verilog-friendly SSH file tools."""

    tool_catalog = (
        ClaudeBashTool,
        _VerilogTextEditorTool,
        ClaudeComputerTool,
        ClaudeMCPProxyTool,
    )


__all__ = ["VerilogClaudeAgent"]
