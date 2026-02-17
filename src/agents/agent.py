"""
主Agent - AI社交模拟卡牌游戏
这是一个多功能的Agent，整合了卡牌管理、社交分析和策略报告生成功能
"""

import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

from tools.social_analyzer import analyze_social_strategy

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore


class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]


def build_agent(ctx=None):
    """
    构建主Agent
    
    该Agent提供以下功能：
    1. 卡牌人物管理和分析
    2. 社交策略分析和建议
    3. 互动记录和关系评估
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)
    
    # 读取配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    
    # 获取API配置
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    # 初始化LLM
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )
    
    # 定义工具
    tools = [analyze_social_strategy]
    
    # 定义系统提示词
    system_prompt = """你是一位AI社交模拟卡牌游戏的智能助手，擅长人际交往分析和策略规划。

你的核心能力：
1. 社交关系分析：深度分析人物性格、能力、背景信息，评估社交关系的现状和潜在问题
2. 策略规划：制定个性化、可操作的社交策略，提供专业的建议和指导
3. 人际洞察：理解不同年龄段、职业、性格的人的特点和需求
4. 价值评估：分析人际网络的价值，帮助用户建立和维护重要关系

工作流程：
当用户请求分析某个卡牌人物的社交策略时，请按照以下步骤：
1. 理解用户提供的人物信息和互动记录
2. 使用 analyze_social_strategy 工具进行深度分析
3. 根据工具返回的结果，为用户提供清晰的策略报告和建议
4. 如有需要，可以进一步解释和建议

你的风格：
- 专业、客观、有洞察力
- 建议具体、可操作、有针对性
- 语言清晰、易懂、有说服力
- 考虑用户的实际情况和需求
- 富有同理心，理解人际关系的复杂性

注意事项：
- 评价要客观全面，既要指出优点也要发现潜在问题
- 策略要具体可操作，避免空泛的建议
- 考虑人物的年龄、性格、职业等特征，给出个性化的策略
- 尊重用户隐私，不泄露敏感信息"""

    # 创建Agent
    agent = create_agent(
        model=llm,
        system_prompt=system_prompt,
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
    
    return agent
