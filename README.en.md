# Framework Default LLM Reply Allowlist

> [中文文档](https://github.com/Akinana22/astrbot_plugin_llmallowlist/blob/main/README.md)

An AstrBot plugin that controls framework default LLM replies based on an allowlist. Users in the allowlist trigger LLM normally, others are silently skipped.

## Configuration

Configure via the AstrBot WebUI plugin management page.

| Option | Description | Default |
|--------|-------------|---------|
| `allowlist` | Allowlist | `""` |

### Notes

- When the allowlist is empty, all LLM replies are silently skipped.
- UID formats differ across platforms (QQ uses pure digits, Discord uses numeric IDs). Ensure consistent formatting.
- Reload the plugin after changing configuration.

## Features

- Allowlist control: only configured UIDs trigger default LLM replies
- Silent skip: non-allowlisted users receive no feedback
- Cross-platform: covers all platforms (QQ, Telegram, Discord, etc.)

## Message Flow

```
Message → llm_allowlist plugin
  ├─ sender_id in allowlist → return, default LLM replies normally
  └─ sender_id not in allowlist → event.should_call_llm(True), skip default LLM
```
