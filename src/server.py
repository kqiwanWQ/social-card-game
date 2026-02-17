"""
AI社交模拟卡牌游戏 - 后端API
提供卡牌管理、互动记录、社交策略分析等功能
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json
import os

from storage.database.supabase_client import get_supabase_client
from agents.social_expert_agent import build_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

# 初始化FastAPI应用
app = FastAPI(title="AI社交模拟卡牌游戏", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# 挂载静态文件服务
if os.path.exists(ASSETS_DIR):
    app.mount("/static", StaticFiles(directory=ASSETS_DIR), name="static")

# 数据模型定义


class CardCreate(BaseModel):
    """创建卡牌的请求模型"""
    photo_url: Optional[str] = None
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    personality: Optional[str] = None
    ability: Optional[str] = None
    bio: Optional[str] = None
    network: Optional[str] = None


class CardUpdate(BaseModel):
    """更新卡牌的请求模型"""
    photo_url: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    personality: Optional[str] = None
    ability: Optional[str] = None
    bio: Optional[str] = None
    network: Optional[str] = None


class InteractionCreate(BaseModel):
    """创建互动记录的请求模型"""
    card_id: int
    interaction_content: str


class StrategyReportResponse(BaseModel):
    """社交策略报告响应模型"""
    id: int
    card_id: int
    current_evaluation: str
    future_strategy: str
    created_at: datetime


# API接口


@app.get("/")
async def root():
    """根路径，返回前端页面"""
    index_path = os.path.join(ASSETS_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return {
            "message": "AI社交模拟卡牌游戏 API",
            "version": "1.0.0",
            "endpoints": {
                "cards": "/api/cards",
                "interactions": "/api/interactions",
                "strategy": "/api/strategy"
            }
        }


# ============ 卡牌管理接口 ============

@app.get("/api/cards")
async def get_cards(search: Optional[str] = Query(None, description="搜索关键词")):
    """
    获取所有卡牌
    - search: 可选，搜索姓名、职业或个人简介
    """
    client = get_supabase_client()
    
    try:
        if search:
            # 搜索功能
            response = client.table('cards').select('*').ilike('name', f'%{search}%').execute()
            if not response.data:
                response = client.table('cards').select('*').ilike('occupation', f'%{search}%').execute()
            if not response.data:
                response = client.table('cards').select('*').ilike('bio', f'%{search}%').execute()
        else:
            response = client.table('cards').select('*').order('created_at', desc=True).execute()
        
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取卡牌列表失败: {str(e)}")


@app.get("/api/cards/{card_id}")
async def get_card(card_id: int):
    """获取单个卡牌的详细信息"""
    client = get_supabase_client()
    
    try:
        response = client.table('cards').select('*').eq('id', card_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="卡牌不存在")
        
        return {"success": True, "data": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取卡牌详情失败: {str(e)}")


@app.post("/api/cards")
async def create_card(card: CardCreate):
    """创建新卡牌"""
    client = get_supabase_client()
    
    try:
        # 验证字段长度
        if card.personality and len(card.personality) > 100:
            raise HTTPException(status_code=400, detail="性格描述不能超过100字")
        if card.ability and len(card.ability) > 100:
            raise HTTPException(status_code=400, detail="能力描述不能超过100字")
        if card.bio and len(card.bio) > 200:
            raise HTTPException(status_code=400, detail="个人简介不能超过200字")
        if card.network and len(card.network) > 200:
            raise HTTPException(status_code=400, detail="人脉关系不能超过200字")
        
        response = client.table('cards').insert({
            "photo_url": card.photo_url,
            "name": card.name,
            "age": card.age,
            "gender": card.gender,
            "occupation": card.occupation,
            "personality": card.personality,
            "ability": card.ability,
            "bio": card.bio,
            "network": card.network
        }).execute()
        
        return {"success": True, "data": response.data[0], "message": "卡牌创建成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建卡牌失败: {str(e)}")


@app.put("/api/cards/{card_id}")
async def update_card(card_id: int, card: CardUpdate):
    """更新卡牌信息"""
    client = get_supabase_client()
    
    try:
        # 验证字段长度
        if card.personality and len(card.personality) > 100:
            raise HTTPException(status_code=400, detail="性格描述不能超过100字")
        if card.ability and len(card.ability) > 100:
            raise HTTPException(status_code=400, detail="能力描述不能超过100字")
        if card.bio and len(card.bio) > 200:
            raise HTTPException(status_code=400, detail="个人简介不能超过200字")
        if card.network and len(card.network) > 200:
            raise HTTPException(status_code=400, detail="人脉关系不能超过200字")
        
        # 构建更新数据（只更新提供的字段）
        update_data = {k: v for k, v in card.model_dump(exclude_unset=True).items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="没有提供要更新的字段")
        
        response = client.table('cards').update(update_data).eq('id', card_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="卡牌不存在")
        
        return {"success": True, "data": response.data[0], "message": "卡牌更新成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新卡牌失败: {str(e)}")


@app.delete("/api/cards/{card_id}")
async def delete_card(card_id: int):
    """删除卡牌"""
    client = get_supabase_client()
    
    try:
        response = client.table('cards').delete().eq('id', card_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="卡牌不存在")
        
        return {"success": True, "message": "卡牌删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除卡牌失败: {str(e)}")


# ============ 互动记录接口 ============

@app.get("/api/cards/{card_id}/interactions")
async def get_interactions(card_id: int):
    """获取某个卡牌的所有互动记录"""
    client = get_supabase_client()
    
    try:
        # 先验证卡牌是否存在
        card_response = client.table('cards').select('id').eq('id', card_id).execute()
        if not card_response.data:
            raise HTTPException(status_code=404, detail="卡牌不存在")
        
        # 获取互动记录
        response = client.table('interactions').select('*').eq('card_id', card_id).order('interaction_date', desc=True).execute()
        
        return {"success": True, "data": response.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取互动记录失败: {str(e)}")


@app.post("/api/interactions")
async def create_interaction(interaction: InteractionCreate):
    """创建新的互动记录"""
    client = get_supabase_client()
    
    try:
        # 验证卡牌是否存在
        card_response = client.table('cards').select('id').eq('id', interaction.card_id).execute()
        if not card_response.data:
            raise HTTPException(status_code=404, detail="卡牌不存在")
        
        # 创建互动记录
        response = client.table('interactions').insert({
            "card_id": interaction.card_id,
            "interaction_content": interaction.interaction_content,
            "interaction_date": datetime.now().isoformat()
        }).execute()
        
        return {"success": True, "data": response.data[0], "message": "互动记录创建成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建互动记录失败: {str(e)}")


@app.delete("/api/interactions/{interaction_id}")
async def delete_interaction(interaction_id: int):
    """删除互动记录"""
    client = get_supabase_client()
    
    try:
        response = client.table('interactions').delete().eq('id', interaction_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="互动记录不存在")
        
        return {"success": True, "message": "互动记录删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除互动记录失败: {str(e)}")


# ============ 社交策略报告接口 ============

@app.get("/api/cards/{card_id}/strategy")
async def get_strategy_report(card_id: int):
    """获取某个卡牌的社交策略报告"""
    client = get_supabase_client()
    
    try:
        # 先验证卡牌是否存在
        card_response = client.table('cards').select('id').eq('id', card_id).execute()
        if not card_response.data:
            raise HTTPException(status_code=404, detail="卡牌不存在")
        
        # 获取最新的策略报告
        response = client.table('strategy_reports').select('*').eq('card_id', card_id).order('created_at', desc=True).limit(1).execute()
        
        if not response.data:
            return {"success": True, "data": None, "message": "暂无社交策略报告"}
        
        return {"success": True, "data": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取社交策略报告失败: {str(e)}")


@app.get("/api/cards/{card_id}/strategy/history")
async def get_strategy_history(card_id: int):
    """获取某个卡牌的所有历史策略报告"""
    client = get_supabase_client()
    
    try:
        # 先验证卡牌是否存在
        card_response = client.table('cards').select('id').eq('id', card_id).execute()
        if not card_response.data:
            raise HTTPException(status_code=404, detail="卡牌不存在")
        
        # 获取所有策略报告
        response = client.table('strategy_reports').select('*').eq('card_id', card_id).order('created_at', desc=True).execute()
        
        return {"success": True, "data": response.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取策略历史失败: {str(e)}")


@app.post("/api/cards/{card_id}/strategy/generate")
async def generate_strategy_report(card_id: int):
    """
    生成社交策略报告
    调用社交专家Agent进行分析，并保存报告到数据库
    """
    client = get_supabase_client()
    
    try:
        # 获取卡牌信息
        card_response = client.table('cards').select('*').eq('id', card_id).execute()
        if not card_response.data:
            raise HTTPException(status_code=404, detail="卡牌不存在")
        
        card = card_response.data[0]
        
        # 获取互动记录
        interactions_response = client.table('interactions').select('*').eq('card_id', card_id).order('interaction_date', desc=True).limit(20).execute()
        interactions = interactions_response.data
        
        # 构建互动记录文本
        interaction_text = "\n".join([
            f"- {item['interaction_date']}: {item['interaction_content']}" 
            for item in interactions
        ])
        
        # 调用社交分析工具（直接调用核心函数）
        from tools.social_analyzer import analyze_social_strategy_core
        
        result = analyze_social_strategy_core(
            card_name=card.get('name', ''),
            card_age=card.get('age'),
            card_gender=card.get('gender'),
            card_occupation=card.get('occupation'),
            card_personality=card.get('personality'),
            card_ability=card.get('ability'),
            card_bio=card.get('bio'),
            card_network=card.get('network'),
            interactions=interaction_text
        )
        
        # 解析结果
        result_data = json.loads(result)
        
        # 保存策略报告到数据库
        report_response = client.table('strategy_reports').insert({
            "card_id": card_id,
            "current_evaluation": result_data.get('current_evaluation', ''),
            "future_strategy": result_data.get('future_strategy', '')
        }).execute()
        
        return {
            "success": True,
            "data": report_response.data[0],
            "message": "社交策略报告生成成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"生成策略报告失败: {str(e)}")


# 启动服务入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
