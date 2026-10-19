# Operations and recovery

Use the selected connection and its recovery behavior. The plugin supplies an HTTP connection to the existing standard Unreal MCP at port 8000. Preserve target project and engine checks. Separately configured project-local bridges are visible only in chats with that trusted project context.

## Native discovery

With tool search on, native `tools/list` exposes `list_toolsets`, `describe_toolset`, and `call_tool`. Toolset actions are dispatched through `call_tool`; missing standalone `BlueprintTools.*` tools are expected. With tool search off, use the actual directly exposed schemas.

A Python-only bridge intentionally exposes different tools. Read `existing-connection.md` instead of trying to repair a registry catalog that the bridge does not publish.

## Console commands

Use these only when the diagnosed issue calls for them:

| Unreal console command | Purpose |
| --- | --- |
| `ModelContextProtocol.StartServer [port]` | Start the server using its established port. |
| `ModelContextProtocol.StopServer` | Stop the server; coordinate with active work before interrupting it. |
| `ModelContextProtocol.RefreshTools` | Refresh toolsets after an authorized plugin/toolset change. |
| `ModelContextProtocol.GenerateClientConfig Codex` | Generate native Codex configuration for an explicit setup task; existing TOML is not overwritten. |

Do not switch tool-search settings, ports, transports, or project plugins just because an individual action fails. Read the returned error and inspect the relevant state first.

## Failure handling

- **No Unreal tools in this chat:** confirm the plugin is enabled, refresh Codex's plugin/MCP discovery or restart it if needed. Its HTTP endpoint requires the expected Unreal Editor to be running. A separate project-local bridge still requires its trusted workspace.
- **Editor unavailable:** verify the configured endpoint and expected project. Wait for an editor restart or ask the user to launch it if it is stopped; do not open a different project to satisfy a probe.
- **Proxy connected, cached catalog visible:** neither proves a live editor connection. `unreal_mcp_status` is proxy state. Verify recovery with an actual read.
- **Native catalog stale after restart:** reconnect the MCP client or reload its tool catalog using the client's available controls. Restart the client only if it cannot refresh. Do not kill a working proxy or add a parallel direct connection as a shortcut.
- **Bridge execute timed out or delivery unknown:** read `get_python_status` using its original UUID. Never automatically resubmit the Python code. Inspect state before proposing a fresh execution if the result is unresolved.
- **Wrong project or engine:** stop that operation and report the mismatch. Do not change the bridge's expected path or version checks without the user requesting a retarget.
- **Toolset absent:** inspect enabled toolsets and the returned registry before proposing configuration changes. Refresh only if a recent toolset change warrants it.
- **Compile, shader, loading, or PIE conflict:** inspect editor state and wait for the current operation. For requested C++ work, discover the actual Live Coding action and check its final diagnostics.

Any mutation that may have completed must be inspected before a retry. Independent read-only checks can be retried with a bound; do not repeatedly poll an unchanged unavailable server.
