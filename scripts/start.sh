#!/bin/bash

# 社交模拟卡牌游戏启动脚本

echo "🎮 正在启动社交模拟卡牌游戏..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查后端服务是否已启动
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ 后端服务已在运行 (http://localhost:8000)"
    echo ""
    echo "📱 请在浏览器中打开: http://localhost:8000/app.html"
    echo "🌐 或者打开: http://localhost:8000/"
else
    # 启动后端服务
    echo "🚀 正在启动后端服务..."
    cd "$(dirname "$0")/.."
    python3 src/server.py > /tmp/social_card_server.log 2>&1 &
    
    # 等待服务启动
    sleep 3
    
    # 检查服务是否启动成功
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ 后端服务启动成功!"
        echo ""
        echo "📱 请在浏览器中打开: http://localhost:8000/app.html"
        echo "🌐 或者打开: http://localhost:8000/"
        echo ""
        echo "📝 查看日志: tail -f /tmp/social_card_server.log"
        echo "🛑 停止服务: pkill -f 'python src/server.py'"
    else
        echo "❌ 后端服务启动失败，请查看日志:"
        echo "   tail -f /tmp/social_card_server.log"
        exit 1
    fi
fi

echo ""
echo "💡 提示："
echo "   - 使用 app.html 体验移动端版本"
echo "   - 使用 index.html 体验桌面版本"
echo "   - 打包成APP请参考 README_MOBILE_APP.md"
