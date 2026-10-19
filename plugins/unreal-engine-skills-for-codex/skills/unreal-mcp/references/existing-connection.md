# Optional request-tracked Python bridges

The plugin's normal route is native Unreal ToolsetRegistry discovery. This reference applies only if the user explicitly selects an existing bridge exposing `get_unreal_connection`, `execute_python`, and `get_python_status`. No Python bridge or custom Unreal toolset is bundled with this plugin.

Bridge implementations differ. Read their exposed schemas and configuration rather than assuming a project path, engine version, endpoint, or custom toolset is available. If a bridge depends on an absent custom Unreal toolset, report that limitation. Do not edit the bridge's expected project or version checks to make a probe succeed.

## Protocol

1. Use the exposed connection check to verify the editor identity before execution.
2. Follow the actual execution schema. Bridges of this shape commonly require exactly one of inline `code` or an absolute `file_path`, plus a fresh UUID `request_id`.
3. Inspect the required Unreal Python APIs with read-only code before editing assets. Work generally runs on Unreal's main thread; split long operations into explicit chunks.
4. If execution is queued, still running, delivery-unknown, or wait-timed-out, query `get_python_status` with the original request ID. Do not automatically resubmit the execution.
5. Continue dependent work only after a successful terminal result. Report failed, rejected, interrupted, or unresolved requests with their ID.

For an authorized editor inspection, a minimal Python read is:

```python
import unreal
print(unreal.SystemLibrary.get_engine_version())
print(unreal.Paths.get_project_file_path())
```

A connected bridge or proxy does not prove that its upstream editor is reachable. Project-scoped MCP entries also require the relevant trusted workspace in Codex. Installing this plugin does not expand the scope of separately configured bridge connections.
