#!/bin/bash

echo "🔍 检查构建是否使用最新代码..."
echo ""

# 检查1：提交历史
echo "📋 检查1：提交历史"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git log --oneline -1
CURRENT_COMMIT=$(git log --oneline -1 | awk '{print $1}')

if [ "$CURRENT_COMMIT" = "33f82d5" ]; then
    echo "✅ 提交正确：33f82d5 docs: 添加正确构建APK指南"
else
    echo "❌ 提交不正确！应该是最新的提交"
    echo ""
    echo "请运行："
    echo "  git pull origin main"
fi
echo ""

# 检查2：app.html大小
echo "📋 检查2：app.html大小"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
APP_HTML_SIZE=$(ls -lh assets/app.html | awk '{print $5}')
echo "app.html 大小: $APP_HTML_SIZE"

if [ "$APP_HTML_SIZE" = "52K" ] || [ "$APP_HTML_SIZE" = "53K" ]; then
    echo "✅ 大小正确（约52KB）"
else
    echo "❌ 大小不正确！应该是约52KB，当前是$APP_HTML_SIZE"
    echo ""
    echo "可能原因："
    echo "  - 没有拉取最新代码"
    echo "  - 文件被意外修改"
fi
echo ""

# 检查3：是否包含设置功能
echo "📋 检查3：是否包含设置功能"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SETTINGS_COUNT=$(grep -c "设置" assets/app.html)
echo "找到 '设置' 关键词次数: $SETTINGS_COUNT"

if [ "$SETTINGS_COUNT" -gt 5 ]; then
    echo "✅ 包含设置功能"
else
    echo "❌ 不包含设置功能或功能不完整"
fi
echo ""

# 检查4：Capacitor同步
echo "📋 检查4：Capacitor同步状态"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ANDROID_APP_HTML_SIZE=$(ls -lh android/app/src/main/assets/public/app.html 2>/dev/null | awk '{print $5}' || echo "不存在")

if [ -z "$ANDROID_APP_HTML_SIZE" ]; then
    echo "❌ Android项目中的app.html不存在"
    echo ""
    echo "请运行："
    echo "  npx cap sync android"
elif [ "$ANDROID_APP_HTML_SIZE" = "$APP_HTML_SIZE" ]; then
    echo "✅ Capacitor已同步（大小一致）"
else
    echo "❌ Capacitor未同步！"
    echo "  assets/app.html: $APP_HTML_SIZE"
    echo "  android/app.html: $ANDROID_APP_HTML_SIZE"
    echo ""
    echo "请运行："
    echo "  npx cap sync android"
fi
echo ""

# 检查5：底部导航
echo "📋 检查5：底部导航"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
BOTTOM_NAV=$(grep -A 5 "bottom-nav" assets/app.html | grep -c "nav-item")

if [ "$BOTTOM_NAV" -gt 0 ]; then
    echo "✅ 包含底部导航"
else
    echo "❌ 不包含底部导航"
fi
echo ""

# 总结
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 检查总结"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$CURRENT_COMMIT" = "33f82d5" ] && [ "$SETTINGS_COUNT" -gt 5 ]; then
    echo "✅ 代码是最新的，包含所有修复"
    echo ""
    echo "下一步："
    echo "  1. 运行: npx cap sync android"
    echo "  2. 运行: cd android && ./gradlew assembleDebug"
    echo "  3. 安装新APK并卸载旧版本"
else
    echo "❌ 代码不是最新的或不完整"
    echo ""
    echo "请执行："
    echo "  1. git pull origin main"
    echo "  2. npx cap sync android"
    echo "  3. cd android && ./gradlew assembleDebug"
fi
