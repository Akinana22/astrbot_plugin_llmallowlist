import re

from astrbot.api import AstrBotConfig
from astrbot.api.event import filter, AstrMessageEvent, MessageChain
from astrbot.api.message_components import Plain, Reply as CompReply, At as CompAt
from astrbot.api.star import Context, Star


class LLMAllowList(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    def _parse_platform_map(self, key):
        raw = self.config.get(key, "")
        if not raw or not raw.strip():
            return {}
        result = {}
        for line in raw.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^(\w+)\[([^\]]*)\]$', line)
            if m:
                platform = m.group(1)
                content = m.group(2).strip()
                result[platform] = content
        return result

    def _parse_allowlist(self):
        pmap = self._parse_platform_map("allowlist")
        return {p: {u.strip() for u in v.split(",") if u.strip()} for p, v in pmap.items()}

    async def _send_reply(self, event: AstrMessageEvent, text: str):
        try:
            mc = MessageChain()
            mc.chain = [CompReply(id=event.message_obj.message_id), Plain(text)]
            await event.send(mc)
        except Exception:
            try:
                mc = MessageChain()
                mc.chain = [CompAt(qq=event.get_sender_id()), Plain(text)]
                await event.send(mc)
            except Exception:
                mc = MessageChain().message(text)
                await event.send(mc)

    @filter.platform_adapter_type(filter.PlatformAdapterType.ALL)
    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_message(self, event: AstrMessageEvent):
        if self.config.get("admin_bypass", False) and event.is_admin():
            return

        sender_id = event.get_sender_id()
        platform = event.get_platform_name()
        allowlist = self._parse_allowlist()

        if sender_id in allowlist.get(platform, set()):
            return

        reply_msgs = self._parse_platform_map("reply_msg")
        reply = reply_msgs.get(platform)
        if reply:
            await self._send_reply(event, reply)

        event.should_call_llm(True)
