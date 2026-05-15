@echo off
REM Windows 启动脚本

cd /d "%~dp0"

REM 创建虚拟环境（如果不存在）
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 启动服务器
echo 启动服务器...
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
