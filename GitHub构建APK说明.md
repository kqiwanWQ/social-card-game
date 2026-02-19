# 🚀 GitHub Actions 快速构建APK

## ✨ 最简单的方法！

我已经为你配置好了GitHub Actions，你只需要几分钟就能得到APK！

---

## 📋 步骤1：创建GitHub仓库（2分钟）

1. 访问 https://github.com/new
2. 填写信息：
   - Repository name: `social-card-game`
   - 选择 **Public**（免费，支持Actions）
   - 不要勾选"Initialize this repository"
3. 点击 "Create repository"

## 📋 步骤2：上传代码（3分钟）

在项目目录执行以下命令：

```bash
# 1. 初始化Git
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Initial commit - Social Card Game"

# 4. 添加远程仓库（替换YOUR_USERNAME）
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/social-card-game.git

# 5. 推送到GitHub
git push -u origin main
```

**注意**：将 `YOUR_USERNAME` 替换为你的GitHub用户名！

## 📋 步骤3：触发构建（1分钟）

### 方式A：自动构建（推荐）

- 推送代码后，GitHub Actions会自动开始构建
- 等待5-10分钟

### 方式B：手动构建

1. 进入你的GitHub仓库
2. 点击 "Actions" 标签
3. 找到 "Build Android APK" 工作流
4. 点击右侧的 "Run workflow" 按钮
5. 选择分支（main）
6. 点击 "Run workflow"
7. 等待5-10分钟

## 📋 步骤4：下载APK（1分钟）

1. 进入 "Actions" 标签
2. 点击最新的构建记录
3. 向下滚动找到 "Artifacts" 部分
4. 点击 "social-card-game-debug" 下载
5. 解压得到 `app-debug.apk`

## 📱 安装到手机

### Android手机安装步骤：

1. **允许安装未知来源应用**
   - 设置 > 安全 > 允许安装未知来源应用
   - 或者在安装时选择"允许"

2. **传输APK到手机**
   - 通过USB、蓝牙、微信、邮件等方式
   - 或直接在手机浏览器中下载

3. **安装APK**
   - 打开APK文件
   - 点击"安装"
   - 等待完成
   - 点击"打开"

4. **首次运行**
   - 系统可能会提示权限
   - 允许网络权限

---

## 🔧 常见问题

### Q1: 推送代码时提示错误

**错误**: `fatal: remote origin already exists`

**解决**:
```bash
# 更新远程仓库地址
git remote set-url origin https://github.com/YOUR_USERNAME/social-card-game.git

# 重新推送
git push -u origin main
```

### Q2: Actions构建失败

**解决**:
1. 查看详细的构建日志
2. 检查是否有错误信息
3. 确保代码已完整上传
4. 尝试重新运行工作流

### Q3: 构建时间太长

**说明**:
- 首次构建需要下载依赖，约10-15分钟
- 后续构建约5-8分钟
- 请耐心等待

### Q4: 下载的APK无法安装

**检查**:
1. 确认APK文件完整
2. 确保已允许安装未知来源应用
3. 尝试使用不同的Android版本
4. 查看手机提示的错误信息

---

## 📊 构建状态

构建过程中你会看到以下步骤：

1. ✅ Checkout code - 检出代码
2. ✅ Set up Node.js - 设置Node.js环境
3. ✅ Install dependencies - 安装依赖
4. ✅ Install Capacitor CLI - 安装Capacitor
5. ✅ Sync Android - 同步Android项目
6. ✅ Build APK - 构建APK
7. ✅ Upload APK - 上传APK

所有步骤完成后，就可以下载APK了！

---

## 🎯 完整命令汇总

```bash
# 一键执行所有步骤
git init && \
git add . && \
git commit -m "Initial commit - Social Card Game" && \
git branch -M main && \
git remote add origin https://github.com/YOUR_USERNAME/social-card-game.git && \
git push -u origin main
```

---

## 📝 提示

1. **修改用户名**：记得将命令中的 `YOUR_USERNAME` 替换成你的GitHub用户名
2. **Public仓库**：选择Public才能免费使用GitHub Actions
3. **等待时间**：首次构建需要10-15分钟，请耐心等待
4. **下载APK**：在Actions页面的Artifacts部分下载

---

## 🎉 成功标志

如果一切顺利，你会看到：

- ✅ GitHub Actions构建成功（绿色对勾）
- ✅ 可以下载APK文件
- ✅ APK大小约10-20MB
- ✅ 可以安装到Android手机

---

**整个过程只需10-15分钟，马上就能得到可用的APK！** 🚀
