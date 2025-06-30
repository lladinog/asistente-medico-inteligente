from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories import FileChatMessageHistory

import os
import json

class Conversation(FileChatMessageHistory):
    def __init__(self, file_path, max_tokens=768, buffer_extra=100):
        super().__init__(file_path)
        self.max_tokens = max_tokens
        self.buffer_extra = buffer_extra  # margen para input + respuesta

    def _count_tokens(self, messages: list[BaseMessage]) -> int:
        return sum(len(m.content.split()) for m in messages if hasattr(m, "content"))

    def _limitar_historial(self):
        while self._count_tokens(self.messages) > (self.max_tokens - self.buffer_extra):
            if self.messages:
                self.messages.pop(0)
            else:
                break
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([m.dict() for m in self.messages], f, ensure_ascii=False, indent=2)

    def add_user_message(self, message: str):
        super().add_user_message(message)
        self._limitar_historial()

    def add_ai_message(self, message: str):
        super().add_ai_message(message)
        self._limitar_historial()
