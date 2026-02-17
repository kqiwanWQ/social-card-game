#!/bin/bash

echo "🔧 连接问题诊断和修复工具"
echo "================================"
echo ""

echo "📊 1. 检查服务状态..."
if ps aux | grep "python src/server.py" | grep -v grep > /dev/null; then
    echo "✅ 服务进程正在运行"
    PID=$(ps aux | grep "python src/server.py" | grep -v grep | awk '{print $2}')
    echo "   进程ID: $PID"
else
    echo "❌ 服务进程未运行"
    echo ""
    echo "🚀 正在启动服务..."
    cd /workspace/projects
    python src/server.py > /tmp/app_server.log 2>&1 &
    sleep 3
    echo "✅ 服务已启动"
fi

echo ""
echo "📊 2. 检查端口状态..."
if lsof -i :8000 > /dev/null 2>&1; then
    echo "✅ 端口 8000 正在监听"
    lsof -i :8000 | grep LISTEN
else
    echo "❌ 端口 8000 未被监听"
    echo ""
    echo "💡 可能的原因："
    echo "   - 端口被其他程序占用"
    echo "   - 服务启动失败"
    echo ""
    echo "🔍 查看占用8000端口的进程："
    lsof -i :8000
fi

echo ""
echo "📊 3. 测试本地连接..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q "200"; then
    echo "✅ 本地连接正常"
else
    echo "❌ 本地连接失败"
    echo "   HTTP响应: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)"
fi

echo ""
echo "📊 4. 检查防火墙..."
if command -v ufw > /dev/null; then
    if ufw status | grep -q "8000"; then
        echo "⚠️  防火墙规则中已找到8000端口"
    else
        echo "💡 防火墙未找到8000端口规则"
        echo "   如果外部无法访问，可能需要开放端口："
        echo "   sudo ufw allow 8000"
    fi
else
    echo "💡 未检测到ufw防火墙"
fi

echo ""
echo "📊 5. 获取可用访问地址..."
echo ""
echo "✅ 可以尝试以下地址："
echo ""

# 获取本机IP地址
if command -v hostname > /dev/null; then
    IP=$(hostname -I | awk '{print $1}')
    if [ ! -z "$IP" ]; then
        echo "   1. 本机访问: http://localhost:8000/"
        echo "   2. 本机访问: http://127.0.0.1:8000/"
        echo "   3. 局域网访问: http://$IP:8000/"
        echo "   4. 局域网访问: http://$IP:8000/app.html (移动版)"
        echo ""
        echo "   💡 如果是容器环境，可能需要使用容器IP: $IP"
    fi
fi

echo ""
echo "📊 6. 检查最近的错误..."
ERROR_COUNT=$(grep -i "error" /tmp/app_server.log | tail -5 | wc -l)
if [ $ERROR_COUNT -gt 0 ]; then
    echo "⚠️  发现最近的错误："
    grep -i "error" /tmp/app_server.log | tail -5
else
    echo "✅ 未发现最近错误"
fi

echo ""
echo "================================"
echo "✅ 诊断完成"
echo ""
echo "💡 如果仍然无法访问，请尝试："
echo ""
echo "1. 清除浏览器缓存后重试"
echo "2. 使用无痕/隐私模式打开"
echo "3. 尝试不同的浏览器（Chrome/Firefox/Edge）"
echo "4. 检查是否有代理或VPN干扰"
echo "5. 尝试使用 http://127.0.0.1:8000/ 而不是 http://localhost:8000/"
echo ""
echo "📝 查看完整日志："
echo "   tail -f /tmp/app_server.log"
echo ""
echo "🔄 重启服务："
echo "   pkill -f 'python src/server.py'"
echo "   ./scripts/start.sh"
