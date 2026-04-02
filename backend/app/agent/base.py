"""
AGENT基类定义
定义所有专业AGENT的通用接口和功能
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_core.messages import BaseMessage


class BaseAgent(ABC):
    """AGENT基类"""

    AGENT_NAME: str = "base_agent"

    @abstractmethod
    async def process(
        self, state: Dict[str, Any], user_input: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        处理输入，返回更新后的状态

        Args:
            state: 当前状态
            user_input: 用户输入（可选）

        Returns:
            更新后的状态
        """
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取AGENT系统提示词"""
        pass

    def _update_state(
        self, state: Dict[str, Any], updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """更新状态"""
        new_state = state.copy()
        new_state.update(updates)
        return new_state

    def _load_history(self, state: Dict[str, Any]) -> list:
        """加载对话历史"""
        messages = state.get("messages", [])
        history = []
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
            elif hasattr(msg, "type"):
                role = msg.type
                content = msg.content if hasattr(msg, "content") else ""
            else:
                continue
            history.append({"role": role, "content": content})
        return history
