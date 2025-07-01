from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_community.chat_message_histories import FileChatMessageHistory
from typing import Optional, List, Dict, Any
import os
import json
import warnings

class Conversation(FileChatMessageHistory):
    def __init__(
        self,
        file_path: str,
        max_context_tokens: int = 768,
        token_buffer: int = 128,
        max_messages: Optional[int] = None,
        tokenizer: Optional[callable] = None,
        encoding: str = "utf-8"
    ):
        """
        Historial de conversación con reescritura completa del JSON.
        
        Args:
            file_path: Ruta del archivo JSON
            max_context_tokens: Límite de tokens del modelo (n_ctx)
            token_buffer: Espacio reservado para respuestas
            max_messages: Límite opcional de mensajes
            tokenizer: Función para contar tokens
            encoding: Codificación del archivo
        """
        self._file_path = file_path
        self._max_context_tokens = max_context_tokens
        self._token_buffer = token_buffer
        self._max_messages = max_messages
        self._tokenizer = tokenizer if tokenizer else lambda x: len(x.split())
        self._encoding = encoding
        self._messages = []

        # Crear directorio y archivo si no existen
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        if not os.path.exists(file_path):
            self._save_messages()
        else:
            self._load_messages()

    def _load_messages(self):
        """Carga mensajes con recreación completa del archivo si hay errores."""
        try:
            with open(self._file_path, 'r', encoding=self._encoding) as f:
                data = json.load(f)
                self._messages = [self._message_from_dict(msg) for msg in data]
        except (json.JSONDecodeError, FileNotFoundError):
            warnings.warn(f"Archivo corrupto o no encontrado en {self._file_path}. Se creará uno nuevo.")
            self._messages = []
            self._save_messages()
        except Exception as e:
            warnings.warn(f"Error al cargar mensajes: {str(e)}. Se reiniciará el historial.")
            self._messages = []
            self._save_messages()

    def _message_from_dict(self, msg_dict: Dict) -> BaseMessage:
        """Convierte dict a BaseMessage."""
        if msg_dict['type'] == 'human':
            return HumanMessage(content=msg_dict['content'])
        elif msg_dict['type'] == 'ai':
            return AIMessage(content=msg_dict['content'])
        return BaseMessage(content=msg_dict['content'])

    def _save_messages(self):
        """Guarda todos los mensajes recreando el archivo completo."""
        try:
            with open(self._file_path, 'w', encoding=self._encoding) as f:
                json.dump([msg.dict() for msg in self._messages], f, ensure_ascii=False, indent=2)
        except Exception as e:
            warnings.warn(f"Error crítico al guardar mensajes: {str(e)}")

    @property
    def messages(self) -> List[BaseMessage]:
        """Devuelve los mensajes actuales."""
        return self._messages.copy()

    def _count_tokens(self, text: str) -> int:
        """Cuenta tokens en un texto usando tokenizer robusto."""
        tokens = self._tokenizer(text)
        if isinstance(tokens, (list, tuple)):
            return len(tokens)
        if hasattr(tokens, "input_ids"):
            return len(tokens.input_ids)
        return int(tokens) if isinstance(tokens, (int, float)) else len(str(tokens).split())


    def _calculate_context_usage(self) -> int:
        """Calcula tokens totales usados."""
        return sum(self._count_tokens(msg.content) for msg in self._messages)

    def _enforce_limits(self):
        """Aplica límites eliminando mensajes antiguos."""
        # 1. Aplicar límite de cantidad de mensajes
        if self._max_messages and len(self._messages) > self._max_messages:
            self._messages = self._messages[-self._max_messages:]

        # 2. Aplicar límite de tokens de contexto
        while len(self._messages) > 1:
            total_tokens = self._calculate_context_usage()
            available_space = self._max_context_tokens - total_tokens
            
            if available_space >= self._token_buffer:
                break
                
            # Eliminar el mensaje más antiguo (excepto el último)
            self._messages.pop(0)

        self._save_messages()

    def add_message(self, message: BaseMessage) -> None:
        """Añade un mensaje gestionando límites."""
        new_tokens = self._count_tokens(message.content)
        max_permitido = self._max_context_tokens - self._token_buffer

        if new_tokens > max_permitido:
            raise ValueError(
                f"Mensaje demasiado largo ({new_tokens} tokens). "
                f"Máximo permitido: {max_permitido}"
            )

        self._messages.append(message)
        self._enforce_limits()

    def add_user_message(self, message: str) -> None:
        """Añade mensaje de usuario."""
        self.add_message(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        """Añade mensaje de asistente."""
        self.add_message(AIMessage(content=message))

    def clear(self) -> None:
        """Limpia completamente el historial."""
        self._messages = []
        self._save_messages()