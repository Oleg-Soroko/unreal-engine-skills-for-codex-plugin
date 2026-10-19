---
name: unreal-mcp
description: Operate or inspect Unreal Editor through an existing MCP connection. Use for Unreal actors, levels, Blueprints, materials, Niagara, Sequencer, widgets, meshes, C++ Live Coding, and editor automation, including UE asset names and .uproject references. Covers native ToolsetRegistry tools and an existing request-tracked Python bridge. Exclude conceptual documentation questions without editor work.
---

# Unreal MCP for Codex

Use the existing Unreal MCP connection to perform the user's editor task. This skill adapts Epic's Unreal MCP workflows for Codex and Unreal 5.8. Respect the project's AGENTS.md and the configured connection's project, engine, execution, and approval constraints.

## Choose the interface actually exposed

Inspect available tools before choosing a route. Codex may prefix server/tool names; resolve the real tools rather than inventing names. This plugin's `unreal` connection uses the already-running native MCP endpoint at `http://127.0.0.1:8000/mcp`; it does not launch an Unreal server or a bridge. Prefer this native route for standard ToolsetRegistry operations. When the user explicitly selects a project-scoped bridge or proxy, preserve that route's checks. Do not register additional connections, change ports, replace a working bridge, or edit .uproject/configuration as part of ordinary editor work.

Before asset changes, confirm that the connected editor targets the Unreal project intended by the user. A port number or cached catalog alone does not identify the active project. Preserve any configured project and engine checks.

### Native ToolsetRegistry route

When `list_toolsets`, `describe_toolset`, and `call_tool` are exposed:

1. Use `list_toolsets` to locate the relevant toolset, or go directly to `describe_toolset` if the domain is known.
2. Read its current schemas. Toolset actions such as `BlueprintTools.create` normally are not individual native tools when tool search is enabled.
3. Dispatch via `call_tool` with the discovered `toolset_name` and matching `arguments`. Pass the action name without its toolset prefix as `tool_name`: for example, schema name `ToolsetRegistry.AgentSkillToolset.ListSkills` means `toolset_name="ToolsetRegistry.AgentSkillToolset"`, `tool_name="ListSkills"`. The tested UE 5.8.3 server rejects a fully qualified `tool_name` as unknown. Do not dispatch `call_tool` through itself. If tool search is disabled and actions are exposed directly, use their actual exposed names/schemas instead.

When `AgentSkillToolset` is available, discover its actual action signatures and read applicable project skills with `ListSkills` / `GetSkills` before unfamiliar project workflows. Missing project skills are not a blocker.

### Existing Python bridge route

If the configured connection instead exposes `get_unreal_connection`, `execute_python`, and `get_python_status`, read [references/existing-connection.md](references/existing-connection.md) and use that route. Do not attempt nonexistent registry tools or connect around the bridge's project/engine checks. Discover the needed Unreal Python API with a small read-only inspection before using it; do not assume an exposed Python class or method exists in this build.

## Editor execution

- Prefer UE conventions for source edits: UObject ownership, UHT reflection, and Slate/UMG as appropriate. Resolve actual asset paths and types before writing.
- Establish a recovery point before bulk asset changes and save completed work using discovered save APIs. Do not treat installation of this plugin as authorization to change project assets.
- Serialize dependent edits and operations touching the same state. Use independent concurrent reads only when the tools support them.
- Check success fields and compilation diagnostics, not just whether the MCP request returned. Stop the affected sequence on a failure; preserve successful earlier work.
- Account for PIE, level loads, and C++/shader compilation. Stop PIE only when needed for the authorized operation. Discover `LiveCodingToolset.CompileLiveCoding` for a requested C++ compile and wait for its reported completion.
- Use available native toolsets for actors, assets, Blueprints, materials, Niagara, animation, Sequencer, widgets, gameplay, and testing. Tool coverage comes from the loaded engine plugins, not this skill.
- For ambiguous delivery or a timeout, inspect state or request status before any mutation is retried. Follow the bridge's no-resubmission rule when using that route.

## Connection and recovery

Do not infer editor reachability from a connected proxy or cached tool catalog. Confirm with a successful live read. Read [references/operations.md](references/operations.md) for missing tools, stale connections, compilation delays, or recovery. Read [references/setup.md](references/setup.md) only for an explicit setup/configuration task or a diagnosed missing connection.

The optional SessionStart hook only supplies project context; the skill is usable without trusting or executing the hook. Never alter hook trust or other runtime permission settings to make it run.
