# AI社交模拟卡牌游戏

一个基于AI的社交关系模拟和策略分析系统，帮助用户管理和分析人际关系，获取专业的社交策略建议。

## 功能特性

### 1. 卡牌人物管理
- ✅ 创建、编辑、删除卡牌人物
- ✅ 记录人物的详细信息：
  - 照片、姓名、年龄、性别、职业
  - 性格描述（<100字）
  - 能力特长（<100字）
  - 个人简介（<200字）
  - 人脉关系（<200字）
- ✅ 支持搜索和浏览

### 2. 互动记录
- ✅ 记录与卡牌人物的日常互动
- ✅ 按时间顺序展示互动历史
- ✅ 支持删除互动记录

### 3. 社交策略分析
- ✅ 基于AI的智能分析，评估当前社交关系
- ✅ 结合人物信息和互动记录，生成专业评价
- ✅ 提供个性化、可操作的社交策略建议
- ✅ 保存历史报告，便于追踪关系发展

## 技术架构

### 后端
- **框架**: FastAPI
- **数据库**: Supabase (PostgreSQL)
- **AI模型**: 豆包 Pro (doubao-seed-2-0-pro-260215)
- **数据表**:
  - `cards`: 存储卡牌人物信息
  - `interactions`: 存储互动记录
  - `strategy_reports`: 存储社交策略报告

### 前端
- **技术**: 纯 HTML/CSS/JavaScript
- **设计**: 竖版移动端友好UI
- **特点**:
  - 渐变色设计，现代美观
  - 响应式布局
  - 流畅的动画效果
  - 模态框交互

## 快速开始

### 1. 启动后端服务

```bash
cd /workspace/projects
python src/server.py
```

服务器将在 `http://localhost:8000` 启动。

### 2. 访问前端页面

打开浏览器访问：
```
http://localhost:8000/
```

或直接打开 `assets/index.html` 文件。

## API接口

### 卡牌管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/cards` | 获取所有卡牌（支持搜索） |
| GET | `/api/cards/{id}` | 获取单个卡牌详情 |
| POST | `/api/cards` | 创建新卡牌 |
| PUT | `/api/cards/{id}` | 更新卡牌信息 |
| DELETE | `/api/cards/{id}` | 删除卡牌 |

### 互动记录

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/cards/{card_id}/interactions` | 获取卡牌的互动记录 |
| POST | `/api/interactions` | 创建互动记录 |
| DELETE | `/api/interactions/{id}` | 删除互动记录 |

### 社交策略

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/cards/{card_id}/strategy` | 获取最新策略报告 |
| GET | `/api/cards/{card_id}/strategy/history` | 获取所有历史报告 |
| POST | `/api/cards/{card_id}/strategy/generate` | 生成新的策略报告 |

## 使用示例

### 示例1：创建卡牌人物

```json
{
  "name": "张三",
  "age": 28,
  "gender": "男",
  "occupation": "软件工程师",
  "personality": "开朗外向，喜欢交朋友",
  "ability": "擅长编程和解决问题",
  "bio": "一名热爱技术的软件工程师，喜欢挑战和创新",
  "network": "在科技公司有广泛的人脉"
}
```

### 示例2：添加互动记录

```json
{
  "card_id": 1,
  "interaction_content": "今天和张三一起讨论了项目进展，他给了我很多有用的建议。"
}
```

### 示例3：生成社交策略报告

点击"社交策略报告"按钮，系统将自动分析并生成报告，包含：
- 当前社交关系评价
- 今后可操作的社交策略

## 项目结构

```
.
├── config/
│   └── agent_llm_config.json       # LLM配置文件
├── src/
│   ├── agents/
│   │   ├── agent.py                # 主Agent
│   │   └── social_expert_agent.py  # 社交专家Agent
│   ├── server.py                   # FastAPI后端服务
│   ├── storage/
│   │   └── database/
│   │       ├── shared/
│   │       │   └── model.py        # 数据库模型
│   │       └── supabase_client.py  # Supabase客户端
│   └── tools/
│       └── social_analyzer.py      # 社交分析工具
└── assets/
    └── index.html                  # 前端页面
```

## 核心功能说明

### 社交分析工具

`src/tools/social_analyzer.py` 提供了核心的社交分析功能：

1. **analyze_social_strategy_core()**: 核心分析函数
   - 接收卡牌人物信息和互动记录
   - 调用LLM进行深度分析
   - 返回JSON格式的策略报告

2. **analyze_social_strategy()**: LangChain工具包装
   - 供Agent调用的工具接口
   - 支持ToolRuntime集成

### 策略报告生成流程

1. 从数据库获取卡牌信息和互动记录
2. 构建人物描述和互动历史
3. 调用LLM进行分析
4. 解析分析结果（当前评价 + 未来策略）
5. 保存报告到数据库
6. 返回给用户

## 注意事项

1. **字段长度限制**:
   - 性格描述：< 100字
   - 能力描述：< 100字
   - 个人简介：< 200字
   - 人脉关系：< 200字

2. **API调用**:
   - 所有API返回JSON格式
   - 成功响应包含 `success: true`
   - 错误响应包含 `detail` 字段

3. **AI分析**:
   - 首次生成策略报告可能需要10-15秒
   - 建议先添加多条互动记录再生成报告
   - 报告会根据人物信息和互动记录个性化定制

## 未来扩展

- [ ] 支持导出策略报告为PDF
- [ ] 添加关系图谱可视化
- [ ] 支持批量导入卡牌
- [ ] 添加社交关系评分系统
- [ ] 支持多人关系网络分析

## 许可证

本项目仅供学习和研究使用。
