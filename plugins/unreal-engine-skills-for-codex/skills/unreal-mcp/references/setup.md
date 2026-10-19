# Codex setup and existing connections

For ordinary tasks, use the plugin's native connection to the current Unreal MCP endpoint. The package declares an HTTP client connection to the existing `http://127.0.0.1:8000/mcp` in `.mcp.json`; it launches no server process and does not edit engine plugins or rewrite existing project/user MCP entries.

## Inspect the current connection first

Codex MCP entries are configured in user or trusted-project `.codex/config.toml`, including stdio bridges and proxies. Use the active workspace's configuration and available tools. A project-local connection is not automatically available in an unrelated projectless chat. Do not interpret that as a broken or absent Unreal setup.

Verify the current editor identity with a read-only operation. If the user selects a separately configured Python bridge, use `existing-connection.md` and preserve its target checks, timeout handling, and project scope.

## Only when new native configuration is requested

The engine must contain enabled `ModelContextProtocol` and `AllToolsets` plugins, or the desired individual toolsets. The MCP server exposes no toolset actions without the corresponding plugins.

From the Unreal Editor console, `ModelContextProtocol.StartServer` starts the server. `ModelContextProtocol.GenerateClientConfig Codex` generates Codex TOML. The generator refuses to overwrite an existing `.codex/config.toml`; merge only the required MCP entry for an authorized setup task. In a source engine checkout, generated configuration belongs at its workspace root; for an installed engine, it belongs beside the .uproject.

For reference, the direct HTTP entry at default settings is:

```toml
[mcp_servers.unreal-mcp]
url = "http://127.0.0.1:8000/mcp"
```

This plugin already supplies that native connection. Do not also add an identical user/project entry. Preserve an explicitly selected proxy or bridge and its authentication. Validate with a live read after the editor is ready.

## Engine auto-start and proxy

If the user requests auto-start, use the per-user project file `Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini`:

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
```

Engine builds may include `Engine/Plugins/Experimental/ModelContextProtocol/Extras/Proxy`. Use the matching build's README for installation. Epic's proxy installer consumes Claude-format `.mcp.json`; do not assume it edits Codex TOML. If the user requests a proxy, use one selected native/proxy route and verify it with an actual read. This plugin requires no additional proxy.
