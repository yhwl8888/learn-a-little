# 家庭教育AI辅导系统

一个功能完整的家庭教育AI辅导平台，包含AI对话、智能出题、拍照批改、错题本、学习计划、诊断报告和知识库等功能。

## 项目结构

```
learn-a-little/
├── frontend/              # 前端代码
│   ├── index.html        # 主页面
│   ├── styles.css        # 样式文件
│   └── app.js            # 前端逻辑
├── backend/              # 后端代码
│   ├── main.py           # FastAPI 主应用
│   └── api/              # API 模块
├── data/                 # 数据目录
│   └── uploads/          # 上传文件存储
├── requirements.txt      # Python 依赖
├── start.sh             # Linux/Mac 启动脚本
└── start.bat            # Windows 启动脚本
```

## 功能特性

1. **AI对话** - 与"小熊老师"进行智能对话
2. **智能出题** - 根据年级和科目生成个性化练习题
3. **拍照批改** - 上传作业照片，自动识别和批改
4. **错题本** - 记录错题，智能分析薄弱点
5. **学习计划** - AI 生成个性化学习计划
6. **诊断报告** - 学习数据分析与提升建议
7. **知识库** - 管理学习资料和知识点

## 快速启动

### 方式一：使用启动脚本（推荐）

Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

Windows:
```cmd
start.bat
```

### 方式二：手动启动

1. 创建虚拟环境：
```bash
python -m venv venv
```

2. 激活虚拟环境：
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate.bat
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 启动服务：
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

5. 打开浏览器访问：http://localhost:8000

## 技术栈

- **前端**：HTML5 + CSS3 + JavaScript（原生 JS，无框架）
- **后端**：FastAPI（Python 3.8+）
- **AI 支持**：集成 Ollama（可选）

## API 端点

- `GET /` - 主页
- `GET /api/children` - 获取孩子列表
- `PUT /api/children/{id}` - 更新孩子信息
- `GET /api/models/list` - 获取可用模型列表
- `GET /api/diagnosis` - 获取诊断数据
- `GET /api/time` - 获取时间信息
- `POST /api/ollama/chat` - AI 聊天接口
- `POST /api/exam/generate` - 生成试卷
- `POST /api/photo` - 上传照片
- `POST /api/photo/grade` - 批改照片
- `POST /api/plan/generate` - 生成学习计划
- `GET /api/kb/list` - 获取知识库列表

## 注意事项

当前版本为演示版本，部分功能使用模拟数据。实际使用时需要：

1. 配置真实的 Ollama 服务
2. 添加数据库支持（如 SQLite/PostgreSQL）
3. 集成 OCR 服务（如 Tesseract 或其他商业 API）
4. 添加用户认证和权限管理

## 开发说明

- 后端代码在 `backend/` 目录
- 前端代码在 `frontend/` 目录
- 上传的文件存储在 `data/uploads/` 目录
