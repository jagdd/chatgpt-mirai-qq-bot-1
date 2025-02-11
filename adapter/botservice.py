from typing import Generator

from loguru import logger


class BotAdapter:
    """定义所有 Chatbot 的通用接口"""
    preset_name: str = "default"

    def get_queue_info(self): ...
    """获取内部队列"""

    def __init__(self, session_id: str = "unknown"):
        self.supported_models = []
        self.current_model = "default"
        ...

    async def ask(self, msg: str) -> Generator[str, None, None]: ...
    """向 AI 发送消息"""

    async def rollback(self): ...
    """回滚对话"""

    async def on_reset(self): ...
    """当会话被重置时，此函数被调用"""

    def use_default_preset_ask(self) -> bool:
        """使用默认预设逻辑"""
        return False

    async def preset_ask(self, role: str, text: str):
        """以预设方式进行提问"""
        if self.use_default_preset_ask():
            if role.endswith('bot') or role in ['assistant', 'chatgpt']:
                logger.debug(f"[预设] 响应：{text}")
                yield text
            else:
                logger.debug(f"[预设] 发送：{text}")
                item = None
                async for item in self.ask(text): ...
                if item:
                    logger.debug(f"[预设] Chatbot 回应：{item}")
                pass  # 不发送 AI 的回应，免得串台
        else:
            yield None

    async def switch_model(self, model_name): ...
    """切换模型"""
