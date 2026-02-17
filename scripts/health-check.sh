#!/bin/bash

echo "🔍 正在检查服务状态..."
echo ""

# 检查端口
if lsof -i :8000 > /dev/null 2>&1; then
    echo "✅ 端口 8000 已被占用（服务正在运行）"
else
    echo "❌ 端口 8000 未被占用（服务未运行）"
    echo ""
    echo "请先启动服务："
    echo "  ./scripts/start.sh"
    echo "  或"
    echo "  python src/server.py"
    exit 1
fi

echo ""
echo "🧪 正在测试API接口..."

# 测试API
API_RESPONSE=$(curl -s http://localhost:8000/api/cards)

if echo "$API_RESPONSE" | grep -q "success"; then
    echo "✅ API接口正常"
else
    echo "❌ API接口异常"
    echo "响应: $API_RESPONSE"
    exit 1
fi

echo ""
echo "🧪 正在测试页面访问..."

# 测试index.html
INDEX_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
if [ "$INDEX_STATUS" = "200" ]; then
    echo "✅ 桌面版页面正常 (http://localhost:8000/)"
else
    echo "❌ 桌面版页面异常 (HTTP $INDEX_STATUS)"
fi

# 测试app.html
APP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/app.html)
if [ "$APP_STATUS" = "200" ]; then
    echo "✅ 移动版页面正常 (http://localhost:8000/app.html)"
else
    echo "❌ 移动版页面异常 (HTTP $APP_STATUS)"
fi

echo ""
echo "✅ 所有检查通过！"
echo ""
echo "📱 访问地址："
echo "  移动端版本: http://localhost:8000/app.html"
echo "  桌面端版本: http://localhost:8000/"
echo ""
echo "📝 查看日志："
echo "  tail -f /tmp/app_server.log"
echo ""
echo "🛑 停止服务："
echo "  pkill -f 'python src/server.py'"
