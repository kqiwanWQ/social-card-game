# 🚀 快速获取APK指南

由于服务器环境限制，推荐在**你的本地电脑**上构建APK（只需5-10分钟）。

---

## 📥 方式一：本地构建（推荐）⭐

### 前提条件

在你的电脑上安装以下工具：

#### Windows系统：
1. **Java 17** 或更高版本
   - 下载：https://adoptium.net/
   - 安装后验证：`java -version`（应该显示17.x.x）

2. **Node.js** (v18或更高版本)
   - 下载：https://nodejs.org/
   - 安装后验证：`node -v` 和 `npm -v`

3. **Android Studio** (可选，推荐用于调试)
   - 下载：https://developer.android.com/studio

#### macOS系统：
```bash
# 使用Homebrew安装
brew install openjdk@17 node
```

#### Linux系统：
```bash
# Ubuntu/Debian
sudo apt install openjdk-17-jdk nodejs npm
```

---

### 构建步骤（超简单）

#### 步骤1：下载项目包

从以下位置下载项目包：
```
/workspace/projects/dist/social-card-game-android.tar.gz (263KB)
```

**或者** 从GitHub下载：
```bash
git clone https://github.com/kqiwanWQ/social-card-game.git
cd social-card-game
```

#### 步骤2：解压并进入目录

```bash
# 解压
tar -xzf social-card-game-android.tar.gz
cd social-card-game-android
```

#### 步骤3：安装依赖

```bash
npm install
```

#### 步骤4：安装Capacitor CLI

```bash
npm install -g @capacitor/cli
```

#### 步骤5：同步Android项目

```bash
npx cap sync android
```

#### 步骤6：构建APK

```bash
# 进入Android目录
cd android

# 赋予执行权限（Linux/Mac）
chmod +x gradlew

# 构建Debug APK
./gradlew assembleDebug
```

**构建时间：** 首次约5-10分钟（下载依赖），后续约1-2分钟

#### 步骤7：找到APK

构建成功后，APK位置：
```
android/app/build/outputs/apk/debug/app-debug.apk
```

**APK信息：**
- 大小：约 8-12 MB
- 最低Android版本：5.0 (API 21)
- 签名：调试签名（可直接安装）

---

### Windows系统特殊说明

在Windows上，使用以下命令：

```cmd
# 步骤1-4同上

# 步骤5：同步Android项目
npx cap sync android

# 步骤6：构建APK
cd android
gradlew.bat assembleDebug
```

---

## 🌐 方式二：使用在线构建服务

如果你不想在本地安装环境，可以使用以下在线服务：

### 1. GitHub Actions（自动）✅

**访问：** https://github.com/kqiwanWQ/social-card-game/actions

**步骤：**
1. 访问仓库的Actions页面
2. 等待构建完成（约5-10分钟）
3. 下载生成的APK

**如果Actions一直没动静：**
- 点击 "Re-run jobs" 重新触发
- 等待几分钟后刷新页面

### 2. Appetize.io（在线测试）

上传APK或项目，在线预览应用：
https://appetize.io/

### 3. Expo Application Services (EAS)

使用Expo构建Android应用：
https://docs.expo.dev/build/introduction/

---

## 📱 安装APK到手机

### Android手机安装步骤

1. **启用未知来源安装**
   ```
   设置 → 安全 → 允许安装未知来源应用
   ```

2. **传输APK到手机**
   - USB数据线连接电脑
   - 或通过微信/QQ/网盘发送
   - 或上传到云盘（百度云、阿里云等）下载

3. **安装APK**
   - 打开APK文件
   - 点击"安装"
   - 完成安装

4. **启动应用**
   - 在应用列表找到"社交卡牌"
   - 点击启动

---

## 🆘 常见问题

### Q1: 构建时提示找不到Java怎么办？
**A:**
```bash
# 检查Java版本
java -version

# 如果不是Java 17，安装Java 17
# Windows: https://adoptium.net/
# Mac: brew install openjdk@17
# Linux: sudo apt install openjdk-17-jdk
```

### Q2: npm install很慢怎么办？
**A: 使用国内镜像**
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

### Q3: Gradle下载很慢怎么办？
**A: 配置Gradle国内镜像**
```bash
# 创建 ~/.gradle/init.gradle 文件
allprojects {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/public' }
        maven { url 'https://maven.aliyun.com/repository/google' }
        mavenCentral()
        google()
    }
}
```

### Q4: 构建失败提示找不到Android SDK？
**A:**
```bash
# 创建 android/local.properties 文件
sdk.dir=/path/to/your/android/sdk

# 或者安装Android Studio，它会自动配置SDK
```

### Q5: APK安装时提示"解析包错误"？
**A:**
1. 确保下载的APK文件完整
2. 检查Android版本是否 >= 5.0
3. 尝试卸载旧版本后再安装

---

## 🎯 推荐流程（最快）

### 如果你已有Node.js和Java环境：

```bash
# 1. 克隆项目
git clone https://github.com/kqiwanWQ/social-card-game.git
cd social-card-game

# 2. 安装依赖
npm install

# 3. 同步Android项目
npx cap sync android

# 4. 构建APK
cd android && ./gradlew assembleDebug

# 5. 安装到手机
# 找到 android/app/build/outputs/apk/debug/app-debug.apk
# 通过USB或微信发送到手机，安装即可！
```

**总时间：约5-10分钟**

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `APK构建指南.md` | 详细构建步骤 |
| `GitHub构建APK说明.md` | GitHub Actions使用指南 |

---

## 💡 提示

1. **首次构建较慢**：需要下载Android SDK和依赖，约5-10分钟
2. **后续构建很快**：依赖已缓存，约1-2分钟
3. **网络问题**：如下载很慢，使用国内镜像（见上方FAQ）
4. **GitHub Actions**：如果本地环境配置麻烦，直接用GitHub Actions

---

## 🎮 应用预览

安装后你将体验：

- 🃏 **卡牌管理**：创建社交关系卡牌
- 💬 **互动记录**：记录每次互动
- 🤖 **AI策略分析**：智能分析社交数据
- 🎨 **游戏化体验**：深色主题、流畅动画

---

## 🎉 开始吧！

选择你最喜欢的方式，5分钟后就能玩到你的社交模拟卡牌游戏！

**有问题随时问我！** 🚀
