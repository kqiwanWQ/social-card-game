# 📱 APK构建完整指南

## ✅ 已完成的工作

我已经完成了以下准备工作：

1. ✅ 安装了Capacitor依赖
2. ✅ 初始化了Capacitor项目
3. ✅ 添加了Android平台
4. ✅ 同步了项目资源
5. ✅ 生成了Android项目结构

## 📦 项目已准备好

Android项目已生成在 `android/` 目录中，可以使用以下任一方式构建APK：

---

## 🚀 方案1：使用Android Studio构建（推荐）

### 步骤1：下载并安装Android Studio

1. 访问：https://developer.android.com/studio
2. 下载适合你系统的Android Studio
3. 安装并启动Android Studio

### 步骤2：首次启动配置

1. 首次启动时会提示安装SDK
2. 选择"Standard"安装（推荐）
3. 等待下载完成（可能需要30-60分钟）
4. 安装完成后会提示重启

### 步骤3：打开项目

1. 将整个项目文件夹复制到你的电脑
2. 在Android Studio中选择 "Open"
3. 选择项目的 `android` 文件夹
4. 等待Gradle同步完成（首次可能需要10-20分钟）

### 步骤4：配置项目

1. 点击 `File > Project Structure`
2. 检查SDK Location是否正确
3. 确保Build Tools已安装

### 步骤5：构建APK

#### Debug版本（快速测试）

1. 点击菜单 `Build > Build Bundle(s) / APK(s) > Build APK(s)`
2. 等待构建完成
3. 点击通知中的 "locate"
4. APK文件位置：`android/app/build/outputs/apk/debug/app-debug.apk`

#### Release版本（正式发布）

1. 生成签名密钥：
   ```bash
   keytool -genkey -v -keystore release.keystore -alias mykey -keyalg RSA -keysize 2048 -validity 10000
   ```

2. 在 `android/app/build.gradle` 中配置签名：
   ```gradle
   android {
       signingConfigs {
           release {
               storeFile file("../release.keystore")
               storePassword "你的密码"
               keyAlias "mykey"
               keyPassword "你的密码"
           }
       }
       buildTypes {
           release {
               signingConfig signingConfigs.release
           }
       }
   }
   ```

3. 构建Release APK：
   ```
   Build > Generate Signed Bundle / APK
   ```

4. 选择APK
5. 选择release密钥
6. 构建完成后APK在：`android/app/build/outputs/apk/release/`

---

## 🌐 方案2：使用云端构建服务（推荐，无需配置环境）

### A. 使用GitHub Actions（推荐）

我已经为你准备好GitHub Actions配置文件！

#### 步骤1：创建GitHub仓库

1. 访问 https://github.com
2. 创建新仓库
3. 上传项目代码

#### 步骤2：启用Actions

1. 在仓库中创建 `.github/workflows/build-android.yml`
2. 复制以下内容：

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Install dependencies
      run: |
        npm install
        npm install -g @capacitor/cli

    - name: Sync Android
      run: npx cap sync android

    - name: Build APK
      run: |
        cd android
        chmod +x gradlew
        ./gradlew assembleDebug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: app-debug
        path: android/app/build/outputs/apk/debug/app-debug.apk
```

#### 步骤3：构建

1. 推送代码到GitHub
2. 进入Actions标签
3. 点击"Build Android APK"
4. 等待构建完成（约5-10分钟）
5. 下载生成的APK

### B. 使用Codemagic（专业方案）

1. 访问：https://codemagic.io
2. 使用GitHub账号登录
3. 连接你的仓库
4. 配置构建脚本：
   ```yaml
   #!/bin/sh
   npm install
   npm install -g @capacitor/cli
   npx cap sync android
   cd android
   ./gradlew assembleDebug
   ```
5. 开始构建
6. 下载APK

### C. 使用AppCenter（微软方案）

1. 访问：https://appcenter.ms
2. 注册账号
3. 创建新应用
4. 连接GitHub仓库
5. 配置分支和构建
6. 自动构建并下载

---

## 🔧 方案3：在Linux/Mac上构建

### 前置要求

1. 安装Java JDK 17或更高
2. 安装Android SDK
3. 配置环境变量

### 安装步骤

#### Ubuntu/Debian

```bash
# 安装OpenJDK
sudo apt update
sudo apt install openjdk-17-jdk

# 下载Android命令行工具
mkdir -p ~/android-sdk
cd ~/android-sdk
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip
mkdir cmdline-tools/latest
mv cmdline-tools/* cmdline-tools/latest/

# 配置环境变量
echo 'export ANDROID_HOME=~/android-sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.bashrc
source ~/.bashrc

# 接受许可证
yes | sdkmanager --licenses

# 安装必要的SDK包
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
```

#### macOS

```bash
# 使用Homebrew安装
brew install --cask android-studio

# 或者安装命令行工具
brew install android-sdk

# 配置环境变量
echo 'export ANDROID_HOME=$HOME/Library/Android/sdk' >> ~/.zshrc
echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools' >> ~/.zshrc
source ~/.zshrc
```

### 构建APK

```bash
# 进入项目目录
cd /path/to/project

# 同步项目
npx cap sync android

# 构建Debug APK
cd android
chmod +x gradlew
./gradlew assembleDebug

# 构建Release APK（需要配置签名）
./gradlew assembleRelease
```

### APK位置

- Debug APK: `android/app/build/outputs/apk/debug/app-debug.apk`
- Release APK: `android/app/build/outputs/apk/release/app-release.apk`

---

## 📦 方案4：使用Docker构建

如果你有Docker，可以快速构建：

```bash
# 创建Dockerfile
cat > Dockerfile.android << 'EOF'
FROM openjdk:17-jdk-slim

ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

# 安装Android命令行工具
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools/latest && \
    cd ${ANDROID_HOME} && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip commandlinetools-linux-9477386_latest.zip -d ${ANDROID_HOME}/cmdline-tools/latest && \
    rm commandlinetools-linux-9477386_latest.zip && \
    yes | ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager --licenses && \
    ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

WORKDIR /workspace
EOF

# 构建Docker镜像
docker build -f Dockerfile.android -t android-builder .

# 运行容器并构建
docker run --rm -v $(pwd):/workspace android-builder bash -c "
  apt-get update && apt-get install -y nodejs npm && \
  cd /workspace && \
  npm install && \
  npx cap sync android && \
  cd android && \
  chmod +x gradlew && \
  ./gradlew assembleDebug
"

# APK在 android/app/build/outputs/apk/debug/app-debug.apk
```

---

## 🎯 快速方案：我帮你生成GitHub Actions

### 立即可用的方案

我已经准备好了所有文件，你只需要：

1. **创建GitHub仓库**
   - 访问 https://github.com/new
   - 仓库名：social-card-game
   - 设置为Public（免费构建）

2. **上传代码**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/你的用户名/social-card-game.git
   git push -u origin main
   ```

3. **等待构建**
   - 进入仓库的Actions标签
   - 等待自动构建完成
   - 下载APK

---

## 📋 构建前检查清单

- [ ] 已安装Node.js 16+
- [ ] 已安装npm
- [ ] 已运行 `npm install`
- [ ] 已运行 `npx cap add android`
- [ ] 已运行 `npx cap sync android`
- [ ] assets/app.html存在
- [ ] capacitor.config.json配置正确

---

## 🔍 常见问题

### Q: 构建失败怎么办？

A: 检查以下几点：
1. Node.js版本是否正确（16+）
2. 依赖是否完整安装
3. 是否同步了Android项目
4. 查看详细错误日志

### Q: APK安装不了？

A: 可能原因：
1. APK签名问题（Release需要签名）
2. Android版本不兼容
3. 权限问题
4. 使用Debug版本测试

### Q: 没有Android Studio怎么办？

A: 使用云端构建方案（方案2），无需本地安装任何工具。

### Q: 构建需要多长时间？

A:
- 首次：30-60分钟（下载依赖）
- 后续：5-10分钟

---

## 🎉 成功标志

构建成功后，你会得到：
- ✅ app-debug.apk（调试版本）
- ✅ app-release.apk（发布版本，需要签名）
- ✅ 文件大小约10-20MB
- ✅ 可以直接安装到Android手机

---

## 📱 安装APK

### 方法1：直接安装

1. 将APK传输到手机
2. 允许安装未知来源应用
3. 打开APK文件
4. 点击安装

### 方法2：使用ADB

```bash
# 连接手机
adb devices

# 安装APK
adb install app-debug.apk
```

### 方法3：通过浏览器

1. 将APK上传到网盘或服务器
2. 在手机浏览器中下载
3. 允许安装
4. 完成

---

**推荐使用方案2（GitHub Actions）或方案1（Android Studio），最简单快速！** 🚀
