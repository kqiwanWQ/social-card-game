"""
社交策略分析工具
使用LLM分析卡牌人物与主角的社交关系，生成社交策略报告
"""

from langchain.tools import tool
from langchain.tools import ToolRuntime
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Optional
import json


def analyze_social_strategy_core(
    card_name: str,
    card_age: Optional[int] = None,
    card_gender: Optional[str] = None,
    card_occupation: Optional[str] = None,
    card_personality: Optional[str] = None,
    card_ability: Optional[str] = None,
    card_bio: Optional[str] = None,
    card_network: Optional[str] = None,
    interactions: str = ""
) -> str:
    """
    社交策略分析的核心函数
    
    Args:
        card_name: 卡牌人物姓名
        card_age: 卡牌人物年龄
        card_gender: 卡牌人物性别
        card_occupation: 卡牌人物职业
        card_personality: 卡牌人物性格（<100字）
        card_ability: 卡牌人物能力（<100字）
        card_bio: 卡牌人物个人简介（<200字）
        card_network: 卡牌人物人脉关系（<200字）
        interactions: 主角与该卡牌人物的互动日常记录
    
    Returns:
        社交策略报告（JSON格式），包含当前评价和今后策略
    """
    ctx = new_context(method="analyze_social_strategy_core")
    
    # 构建系统提示词
    system_prompt = """你是一位资深的高情商社交专家，擅长人际交往分析和策略规划。

你的任务是：
1. 基于卡牌人物的个人信息（姓名、年龄、性别、职业、性格、能力、简介、人脉）
2. 结合主角与该人物的互动日常记录
3. 进行深度诊断分析
4. 给出当前社交关系的客观评价
5. 制定今后的社交策略报告

输出要求：
- 评价要客观、全面，既要指出优点也要发现潜在问题
- 策略要具体、可操作，避免空泛的建议
- 考虑人物的年龄、性格、职业等特征，给出个性化的策略
- 格式清晰，结构分明，易于理解

输出格式（JSON）：
{
  "current_evaluation": "当前社交关系评价（200-500字）",
  "future_strategy": "今后社交策略（500-800字）"
}"""

    # 构建人物信息描述
    card_info = f"""人物信息：
- 姓名：{card_name}
- 年龄：{card_age if card_age else '未知'}
- 性别：{card_gender if card_gender else '未知'}
- 职业：{card_occupation if card_occupation else '未知'}
- 性格：{card_personality if card_personality else '无描述'}
- 能力：{card_ability if card_ability else '无描述'}
- 个人简介：{card_bio if card_bio else '无描述'}
- 人脉关系：{card_network if card_network else '无描述'}"""

    # 构建用户提示词
    user_prompt = f"""请分析以下人物的社交情况并给出策略建议：

{card_info}

互动日常记录：
{interactions if interactions else '暂无互动记录'}

请根据以上信息，给出当前评价和今后的社交策略。输出必须为JSON格式。"""

    try:
        # 初始化LLM客户端
        client = LLMClient(ctx=ctx)
        
        # 构建消息
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        # 调用LLM
        response = client.invoke(
            messages=messages,
            model="doubao-seed-2-0-pro-260215",
            temperature=0.7,
            max_completion_tokens=2000
        )
        
        # 提取文本内容
        def get_text_content(content):
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                if content and isinstance(content[0], str):
                    return " ".join(content)
                else:
                    return " ".join(item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text")
            return str(content)
        
        result_text = get_text_content(response.content)
        
        # 尝试解析JSON
        try:
            # 尝试直接解析
            result = json.loads(result_text)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON部分
            import re
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # 如果还是失败，返回原始文本
                result = {
                    "current_evaluation": "分析结果生成失败，请重试。",
                    "future_strategy": result_text
                }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_result = {
            "current_evaluation": f"分析过程中出现错误：{str(e)}",
            "future_strategy": "请检查输入信息是否完整，或稍后重试。"
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)


@tool
def analyze_social_strategy(
    card_name: str,
    card_age: Optional[int] = None,
    card_gender: Optional[str] = None,
    card_occupation: Optional[str] = None,
    card_personality: Optional[str] = None,
    card_ability: Optional[str] = None,
    card_bio: Optional[str] = None,
    card_network: Optional[str] = None,
    interactions: str = "",
    runtime: ToolRuntime = None
) -> str:
    """
    分析主角与卡牌人物之间的社交关系，生成社交策略报告
    
    Args:
        card_name: 卡牌人物姓名
        card_age: 卡牌人物年龄
        card_gender: 卡牌人物性别
        card_occupation: 卡牌人物职业
        card_personality: 卡牌人物性格（<100字）
        card_ability: 卡牌人物能力（<100字）
        card_bio: 卡牌人物个人简介（<200字）
        card_network: 卡牌人物人脉关系（<200字）
        interactions: 主角与该卡牌人物的互动日常记录
        runtime: ToolRuntime对象（用于Agent调用）
    
    Returns:
        社交策略报告（JSON格式），包含当前评价和今后策略
    """
    return analyze_social_strategy_core(
        card_name=card_name,
        card_age=card_age,
        card_gender=card_gender,
        card_occupation=card_occupation,
        card_personality=card_personality,
        card_ability=card_ability,
        card_bio=card_bio,
        card_network=card_network,
        interactions=interactions
    )
