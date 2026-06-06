import re

from astrbot.api import AstrBotConfig
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star


class LLMAllowList(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    def _parse_allowlist(self):
        raw = self.config.get("allowlist", "")
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
                uids = {u.strip() for u in m.group(2).split(",") if u.strip()}
                result[platform] = uids
        return result

    @filter.platform_adapter_type(filter.PlatformAdapterType.ALL)
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        sender_id = event.get_sender_id()
        platform = event.get_platform_name()
        allowlist = self._parse_allowlist()

        if sender_id in allowlist.get(platform, set()):
            return

        event.should_call_llm(True)
