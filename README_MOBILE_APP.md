# 社交模拟卡牌 - 移动APP

一个基于AI的社交关系模拟游戏化APP，帮助用户以游戏的方式管理和分析人际关系，获取专业的社交策略建议。

## 🎮 功能特性

### 核心功能
- ✨ **卡牌人物管理** - 创建、编辑、删除卡牌人物，记录详细信息
- 📝 **互动记录** - 记录与卡牌人物的日常互动，按时间顺序展示
- 🎯 **AI策略分析** - 基于AI智能分析，生成个性化社交策略报告
- 🔍 **智能搜索** - 快速搜索和浏览卡牌人物
- 📊 **统计功能** - 查看卡牌总数和互动次数

### 游戏化体验
- 🎨 **精美UI设计** - 深色主题、渐变色彩、玻璃拟态效果
- ✨ **流畅动画** - 卡牌脉冲、模态框滑入、按钮反馈
- 🎵 **触觉反馈** - 按钮点击、操作成功时的震动反馈
- 📱 **原生体验** - 沉浸式状态栏、底部导航、手势支持
- 🌙 **暗黑模式** - 护眼深色主题，适合夜间使用

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装Node.js依赖
npm install

# 安装Capacitor
npm install @capacitor/cli @capacitor/core
npx cap init
```

### 2. 启动后端服务

```bash
# 方式1：使用npm脚本
npm start

# 方式2：直接运行Python
python src/server.py
```

后端服务将在 `http://localhost:8000` 启动。

### 3. 访问应用

#### Web版本
打开浏览器访问：
```
http://localhost:8000/
```

#### 移动APP版本
```bash
# 同步Capacitor
npm run sync

# 在Android Studio中打开
npm run android

# 在Xcode中打开
npm run ios
```

## 📱 打包成原生APP

### Android打包

1. **安装Android Studio**
   - 下载并安装最新版Android Studio
   - 配置Android SDK（建议API 33+）

2. **同步项目**
   ```bash
   npm run sync
   ```

3. **打开项目**
   ```bash
   npm run android
   ```

4. **在Android Studio中**
   - 点击 `Build > Generate Signed Bundle/APK`
   - 选择 `APK`
   - 创建或选择密钥库
   - 选择 `release` 构建类型
   - 点击 `Finish`

5. **安装到设备**
   - 将生成的APK文件传输到手机
   - 允许安装未知来源应用
   - 安装APK即可使用

### iOS打包

1. **安装Xcode**
   - 确保安装了最新版Xcode（14.0+）
   - 配置Apple开发者账号

2. **同步项目**
   ```bash
   npm run sync
   ```

3. **打开项目**
   ```bash
   npm run ios
   ```

4. **在Xcode中**
   - 选择目标设备或模拟器
   - 点击 `Product > Archive`
   - 在Organizer窗口中选择 `Distribute App`
   - 选择分发方式（App Store / Ad Hoc / Enterprise）
   - 按照提示完成签名和上传

### 使用云端打包（推荐）

如果你没有配置好开发环境，可以使用以下云端打包服务：

- **[AppCenter](https://appcenter.ms)** - Microsoft的云端打包服务
- **[Codemagic](https://codemagic.io)** - 专业的移动端CI/CD服务
- **[GitHub Actions](https://github.com/features/actions)** - GitHub的自动化构建服务

## 🎨 应用截图

### 主界面
- 卡牌列表展示
- 顶部统计信息
- 搜索功能
- 添加卡牌按钮

### 卡牌详情
- 人物头像和信息
- 互动记录列表
- 社交策略报告
- 操作按钮（互动、分析、编辑、删除）

### 社交策略报告
- 当前关系评价
- 今后可操作策略
- 个性化建议

## 🔧 配置说明

### Capacitor配置

`capacitor.config.json` 文件包含以下配置：

```json
{
  "appId": "com.socialcard.game",      // 应用包名
  "appName": "社交模拟卡牌",            // 应用名称
  "webDir": "assets",                   // Web资源目录
  "server": {
    "androidScheme": "https"            // Android使用HTTPS
  },
  "plugins": {
    "SplashScreen": {
      "launchShowDuration": 2000,       // 启动页显示时长
      "backgroundColor": "#1a1a2e",     // 背景颜色
      "spinnerColor": "#ffd700"         // 加载动画颜色
    }
  }
}
```

### API配置

后端API地址在 `assets/app.html` 中配置：

```javascript
const API_BASE = 'http://localhost:8000/api';
```

**注意**：打包成APP后，如果后端在本地运行，需要将 `localhost` 替换为设备的实际IP地址：

```javascript
// 开发环境
const API_BASE = 'http://YOUR_PC_IP:8000/api';

// 生产环境
const API_BASE = 'https://your-domain.com/api';
```

## 🎮 游戏化特性说明

### 视觉设计
- **深色主题** - 采用深蓝紫色调，符合现代游戏审美
- **玻璃拟态** - 半透明背景 + 模糊效果，增强层次感
- **渐变色彩** - 按钮和头像使用金色渐变，突出重点
- **圆角设计** - 所有元素使用大圆角，更加柔和友好

### 动画效果
- **脉冲动画** - 卡牌头像呼吸效果，增强活力
- **滑入动画** - 模态框从底部滑入，符合移动端习惯
- **缩放反馈** - 按钮点击时缩放，提供触觉反馈
- **渐变光效** - 按钮悬停时的光效，增强交互感

### 交互优化
- **大触摸区域** - 所有按钮和卡牌都有足够大的触摸区域
- **快速响应** - 所有操作都有即时反馈（Toast提示）
- **流畅滚动** - 列表滚动平滑，支持惯性滚动
- **底部导航** - 符合移动端用户习惯的导航方式

## 📊 数据库表结构

### cards（卡牌表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| photo_url | String(500) | 照片URL |
| name | String(100) | 姓名 |
| age | Integer | 年龄 |
| gender | String(20) | 性别 |
| occupation | String(100) | 职业 |
| personality | Text | 性格（<100字） |
| ability | Text | 能力（<100字） |
| bio | Text | 个人简介（<200字） |
| network | Text | 人脉关系（<200字） |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### interactions（互动记录表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| card_id | Integer | 关联卡牌ID |
| interaction_content | Text | 互动内容 |
| interaction_date | DateTime | 互动日期 |
| created_at | DateTime | 创建时间 |

### strategy_reports（策略报告表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| card_id | Integer | 关联卡牌ID |
| current_evaluation | Text | 当前评价 |
| future_strategy | Text | 今后策略 |
| created_at | DateTime | 创建时间 |

## 🔒 安全说明

1. **API安全**
   - 生产环境建议使用HTTPS
   - 添加API认证机制
   - 实施请求频率限制

2. **数据安全**
   - 敏感信息加密存储
   - 定期备份数据
   - 实施访问控制

3. **用户隐私**
   - 不要收集不必要的个人信息
   - 提供数据删除功能
   - 遵守相关法律法规

## 🚀 性能优化

### 前端优化
- 图片懒加载
- 代码压缩和混淆
- 使用CDN加速静态资源
- 实现离线缓存（Service Worker）

### 后端优化
- 数据库查询优化
- 添加缓存机制
- 使用异步处理
- 负载均衡

## 🐛 常见问题

### Q: APK无法安装？
A: 检查是否允许安装未知来源应用，在设置中开启。

### Q: APP无法连接到后端？
A: 确保手机和电脑在同一网络，使用电脑的实际IP地址。

### Q: iOS打包失败？
A: 检查Xcode版本和签名配置，确保有有效的开发者账号。

### Q: 策略报告生成很慢？
A: 首次生成需要调用AI模型，可能需要10-15秒，后续会更快。

## 📈 后续规划

### 功能扩展
- [ ] 多语言支持（英文、日文等）
- [ ] 社交关系图谱可视化
- [ ] 批量导入/导出卡牌
- [ ] 社交关系评分系统
- [ ] 提醒功能（定期提醒互动）
- [ ] 数据统计和图表

### 体验优化
- [ ] 更多动画效果
- [ ] 音效反馈
- [ ] 手势操作（左滑删除等）
- [ ] 深色/浅色主题切换
- [ ] 自定义主题颜色

## 📞 技术支持

如有问题，请通过以下方式联系：
- GitHub Issues
- 邮件：support@example.com

## 📄 许可证

本项目仅供学习和研究使用。

## 🙏 致谢

感谢以下开源项目：
- [Capacitor](https://capacitorjs.com/) - 跨平台原生运行时
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Web框架
- [Supabase](https://supabase.com/) - 开源Firebase替代品
- [LangChain](https://langchain.com/) - AI应用开发框架

---

**享受你的社交模拟游戏体验！** 🎮✨
