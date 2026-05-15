#!/bin/bash
# 启动脚本

# 设置工作目录
cd "$(dirname "$0")"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 启动服务器
echo "启动服务器..."
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
