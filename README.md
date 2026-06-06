# 框架默认LLM回复白名单

> [English Documentation](https://github.com/Akinana22/astrbot_plugin_llmallowlist/blob/main/README.en.md)

AstrBot 插件。根据白名单控制框架默认 LLM 回复，白名单内用户正常触发 LLM，其余静默跳过。

## 配置

在 AstrBot WebUI 插件管理页面配置。

| 配置 | 说明 | 默认值 |
|------|------|--------|
| `allowlist` | 白名单 | `""` |

### 注意事项

- 白名单为空时，所有用户的 LLM 回复均被静默跳过。
- 不同平台的 UID 格式不同（QQ 为纯数字、Discord 为数字 ID），配置时注意格式统一。
- 配置修改后需重新加载插件生效。

## 功能

- 白名单控制：仅配置中的 UID 可触发默认 LLM 回复
- 无感知静默：非白名单用户消息被静默跳过，无任何回复
- 全平台兼容：覆盖所有平台（QQ、Telegram、Discord 等）

## 消息流转

```
消息 → llm_allowlist 插件
  ├─ sender_id 在白名单中 → return，默认 LLM 正常回复
  └─ sender_id 不在白名单中 → event.should_call_llm(True)，跳过默认 LLM
```
