@echo off
chcp 65001 > nul
echo 🎮 正在启动社交模拟卡牌游戏...

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装，请先安装Python
    pause
    exit /b 1
)

REM 检查后端服务是否已启动
netstat -ano | findstr :8000 | findstr LISTENING >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ 后端服务已在运行 ^(http://localhost:8000^)
    echo.
    echo 📱 请在浏览器中打开: http://localhost:8000/app.html
    echo 🌐 或者打开: http://localhost:8000/
) else (
    REM 启动后端服务
    echo 🚀 正在启动后端服务...
    cd /d "%~dp0.."
    start /B python src/server.py > temp\social_card_server.log 2>&1
    
    REM 等待服务启动
    timeout /t 3 /nobreak >nul
    
    REM 检查服务是否启动成功
    netstat -ano | findstr :8000 | findstr LISTENING >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ 后端服务启动成功!
        echo.
        echo 📱 请在浏览器中打开: http://localhost:8000/app.html
        echo 🌐 或者打开: http://localhost:8000/
        echo.
        echo 📝 查看日志: type temp\social_card_server.log
        echo 🛑 停止服务: taskkill /F /IM python.exe
    ) else (
        echo ❌ 后端服务启动失败，请查看日志:
        echo    type temp\social_card_server.log
        pause
        exit /b 1
    )
)

echo.
echo 💡 提示:
echo    - 使用 app.html 体验移动端版本
echo    - 使用 index.html 体验桌面版本
echo    - 打包成APP请参考 README_MOBILE_APP.md
echo.

pause
