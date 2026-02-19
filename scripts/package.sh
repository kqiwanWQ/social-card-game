#!/bin/bash

echo "📦 正在打包Android项目..."
echo ""

PROJECT_DIR="/workspace/projects"
PACKAGE_DIR="$PROJECT_DIR/dist"
ANDROID_DIR="$PROJECT_DIR/android"
PACKAGE_NAME="social-card-game-android"

# 创建输出目录
mkdir -p "$PACKAGE_DIR"

# 复制必要文件
echo "📁 复制项目文件..."

# 创建临时目录
TEMP_DIR="$PACKAGE_DIR/$PACKAGE_NAME"
mkdir -p "$TEMP_DIR"

# 复制Android项目
cp -r "$ANDROID_DIR" "$TEMP_DIR/"

# 复制配置文件
cp "$PROJECT_DIR/capacitor.config.json" "$TEMP_DIR/"
cp "$PROJECT_DIR/package.json" "$TEMP_DIR/"

# 复制assets（Web资源）
cp -r "$PROJECT_DIR/assets" "$TEMP_DIR/"

# 创建README
cat > "$TEMP_DIR/README.md" << 'EOF'
# 社交模拟卡牌 - Android项目

## 📱 安装APK

如果项目中已包含APK文件，直接安装即可。

否则，请使用Android Studio构建：

### 使用Android Studio构建

1. 打开Android Studio
2. 选择 "Open"
3. 选择 `android` 文件夹
4. 等待Gradle同步完成
5. 点击 `Build > Build Bundle(s) / APK(s) > Build APK(s)`
6. APK文件位置：`android/app/build/outputs/apk/debug/app-debug.apk`

### 快速构建命令

在项目根目录执行：

```bash
# 同步项目
npx cap sync android

# 构建APK
cd android
./gradlew assembleDebug
```

## 📚 更多信息

- 完整构建指南：查看项目根目录的 `APK构建指南.md`
- GitHub Actions：查看项目根目录的 `GitHub构建APK说明.md`

## 🎮 应用功能

- 卡牌人物管理
- 互动记录
- AI社交策略分析
- 游戏化UI设计
- 移动端优化

---

**享受你的社交模拟游戏体验！** 🎮✨
EOF

# 创建构建脚本
cat > "$TEMP_DIR/build-apk.sh" << 'EOF'
#!/bin/bash

echo "🚀 开始构建APK..."
echo ""

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装，请先安装Node.js"
    exit 1
fi

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm未安装，请先安装npm"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
npm install

# 安装Capacitor CLI
echo "📦 安装Capacitor CLI..."
npm install -g @capacitor/cli

# 同步Android项目
echo "🔄 同步Android项目..."
npx cap sync android

# 构建APK
echo "🔨 构建APK..."
cd android
chmod +x gradlew
./gradlew assembleDebug

# APK位置
APK_PATH="app/build/outputs/apk/debug/app-debug.apk"

if [ -f "$APK_PATH" ]; then
    echo ""
    echo "✅ APK构建成功！"
    echo "📦 APK位置: $APK_PATH"
    echo ""
    echo "💡 可以将此APK传输到手机安装"
else
    echo ""
    echo "❌ APK构建失败"
    exit 1
fi
EOF

chmod +x "$TEMP_DIR/build-apk.sh"

# 打包成tar.gz
echo "📦 打包成TAR.GZ文件..."
cd "$PACKAGE_DIR"
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"

echo ""
echo "✅ 打包完成！"
echo ""
echo "📦 包位置: $PACKAGE_DIR/${PACKAGE_NAME}.tar.gz"
echo ""
echo "📝 包含内容："
echo "  - Android项目源码"
echo "  - Web资源文件"
echo "  - 构建脚本"
echo "  - README说明"
echo ""
echo "🚀 使用方法："
echo "  1. 下载ZIP文件"
echo "  2. 解压到本地"
echo "  3. 在Android Studio中打开 android 文件夹"
echo "  4. 或者运行 build-apk.sh 构建APK"
echo ""
echo "📱 如果APK已构建完成："
echo "  - 位于: android/app/build/outputs/apk/debug/app-debug.apk"
echo "  - 可以直接安装到手机"
