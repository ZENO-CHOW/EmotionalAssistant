"""
消息总线
AGENT间通信机制
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """消息类型"""

    STATE_UPDATE = "state_update"
    AGENT_REQUEST = "agent_request"
    AGENT_RESPONSE = "agent_response"
    USER_INPUT = "user_input"
    SESSION_END = "session_end"


@dataclass
class AgentMessage:
    """AGENT间消息"""

    sender: str
    receiver: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "message_type": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }


class MessageBus:
    """消息总线"""

    def __init__(self):
        self.subscribers: Dict[str, list] = {}
        self.message_history: list = []

    def subscribe(self, agent_name: str, callback):
        """订阅消息"""
        if agent_name not in self.subscribers:
            self.subscribers[agent_name] = []
        self.subscribers[agent_name].append(callback)
        logger.info(f"Agent {agent_name} 已订阅消息总线")

    def unsubscribe(self, agent_name: str, callback):
        """取消订阅"""
        if agent_name in self.subscribers:
            if callback in self.subscribers[agent_name]:
                self.subscribers[agent_name].remove(callback)
                logger.info(f"Agent {agent_name} 已取消订阅")

    def publish(self, message: AgentMessage):
        """发布消息"""
        self.message_history.append(message)
        receiver = message.receiver
        if receiver in self.subscribers:
            for callback in self.subscribers[receiver]:
                try:
                    callback(message)
                except Exception as e:
                    logger.error(f"消息处理失败: {str(e)}")

    def send_message(
        self,
        sender: str,
        receiver: str,
        message_type: MessageType,
        content: Dict[str, Any],
    ) -> AgentMessage:
        """发送消息"""
        message = AgentMessage(
            sender=sender, receiver=receiver, message_type=message_type, content=content
        )
        self.publish(message)
        return message

    def get_history(self, agent_name: Optional[str] = None) -> list:
        """获取消息历史"""
        if agent_name:
            return [
                m
                for m in self.message_history
                if m.sender == agent_name or m.receiver == agent_name
            ]
        return self.message_history


message_bus = MessageBus()
