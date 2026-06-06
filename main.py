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
            return set()
        return {uid.strip() for uid in raw.split(",") if uid.strip()}

    @filter.platform_adapter_type(filter.PlatformAdapterType.ALL)
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        sender_id = event.get_sender_id()
        allowlist = self._parse_allowlist()

        if sender_id in allowlist:
            return

        event.should_call_llm(True)
