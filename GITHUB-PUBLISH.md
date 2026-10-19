# Публикация unreal-engine-skills-for-codex-plugin

## Позиционирование

Репозиторий: **[Oleg-Soroko/unreal-engine-skills-for-codex-plugin](https://github.com/Oleg-Soroko/unreal-engine-skills-for-codex-plugin)**.

Название в интерфейсе: **Unreal Engine Skills for Codex**.

Description для блока About:

> Unofficial Codex adaptation of Epic Games' Unreal Engine skills. Control Unreal Editor through its native MCP server.

Topics: `unreal-engine`, `codex`, `mcp`, `agent-skills`, `unreal-engine-5`, `developer-tools`.

Ссылка на оригинал уже стоит в первом абзаце README и в Credits. Авторство Epic, исходная MIT-лицензия, версия и commit оригинала сохранены. Авторство адаптации указано отдельно. Локальные пути и сведения о личном проекте удалены из публичного пакета.

## Обновление репозитория

Репозиторий использует ветку `main`. Перед отправкой обнови README, если изменились основные возможности, установка или управление. Проверь все изменения проекта, включая файлы в `.agents` и внутри папки плагина.

```powershell
git config user.name olegsoroko
git config user.email oleg.soroko@gmail.com
git status --short
git add .
git diff --cached --check
git diff --cached --stat
git commit -m "Describe the concrete plugin change"
git push -u origin main
```

Для отправки используй авторизацию GitHub аккаунта `Oleg-Soroko`, владеющего этим репозиторием. Имя автора коммитов настроено как `olegsoroko`, email — `oleg.soroko@gmail.com`.

Description и Topics для блока About приведены выше. После проверки версии можно создать Release `v1.0.0` с описанием ниже. ZIP с исходниками можно приложить к Release; исходный код находится в самом репозитории.

## Короткое объявление на английском

> I adapted Epic Games' Unreal Engine Skills for Claude Code into an unofficial Codex plugin. It uses Unreal's existing native MCP server and includes Codex-specific workflows, tool discovery, recovery guidance, and an optional Windows startup hook. Original skills and workflow foundation by Epic Games; Codex adaptation by Oleg Soroko. MIT licensed.

## Описание первого Release

### Unreal Engine Skills for Codex — v1.0.0

Unofficial Codex adaptation of Epic Games' Unreal Engine Skills for Claude Code.

- Codex plugin packaging and local marketplace installation.
- Native Unreal MCP discovery and project Agent Skills.
- Codex-specific workflow and recovery instructions.
- Optional Windows startup context hook.
- Tested plugin loading and read-only MCP operations with Unreal 5.8.3.

Original project: https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin

This is a community adaptation, not an official Epic Games or OpenAI release. MIT licensed; upstream attribution is preserved. Asset-editing workflows have not been exhaustively tested.
