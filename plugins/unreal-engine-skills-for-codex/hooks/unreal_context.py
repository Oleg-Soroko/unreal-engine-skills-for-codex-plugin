"""Read-only Codex SessionStart context, adapted from Epic's Bash hook."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tomllib

GENERATORS = ("GenerateProjectFiles.bat", "GenerateProjectFiles.sh", "GenerateProjectFiles.command")


def configured_unreal(directory: Path) -> bool:
    # A global home config is not evidence that an unrelated workspace is Unreal.
    if directory == Path.home():
        return False
    config = directory / ".codex/config.toml"
    try:
        data = tomllib.loads(config.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return False
    for name, entry in data.get("mcp_servers", {}).items():
        if not isinstance(entry, dict) or entry.get("enabled") is False:
            continue
        values = [name, entry.get("command", ""), *entry.get("args", [])]
        if any("unreal" in str(value).lower() for value in values):
            return True
    return False


def context_for(cwd: Path) -> str | None:
    directory = cwd.resolve()
    for candidate in (directory, *directory.parents):
        try:
            projects = sorted(p.name for p in candidate.glob("*.uproject") if p.is_file())
            source_tree = any((candidate / name).is_file() for name in GENERATORS)
            bridge = configured_unreal(candidate)
        except OSError:
            continue
        if not projects and not source_tree and not bridge:
            continue
        parts = ["This workspace contains an Unreal Engine project or a configured Unreal MCP connection."]
        if projects:
            parts.append("Project file(s): " + ", ".join(projects) + ".")
        if source_tree:
            parts.append("An Unreal Engine source root was detected.")
        parts.append("Use $unreal-mcp for live editor work. Prefer Unreal C++/UObject, UHT, and Slate/UMG conventions where applicable.")
        parts.append("Reuse the project's existing MCP connection and its target checks. Inspect the exposed tools before choosing native registry calls or the request-tracked Python bridge.")
        return " ".join(parts)
    return None


def main() -> None:
    event = {}
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
            if raw.strip():
                event = json.loads(raw)
    except (OSError, ValueError):
        pass
    if not isinstance(event, dict):
        event = {}
    cwd = event.get("cwd") or os.getcwd()
    if not isinstance(cwd, str):
        return
    try:
        context = context_for(Path(cwd))
    except (OSError, ValueError):
        return
    if context:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": context
        }}, ensure_ascii=True))


if __name__ == "__main__":
    main()
