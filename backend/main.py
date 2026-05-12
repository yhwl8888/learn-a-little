from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import os
import json
import httpx
import asyncio
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import random
import calendar

# 导入我们的模块
from api import children, models, diagnosis, time_api, exam, photo, plan, kb

app = FastAPI(title="家庭教育AI辅导")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件目录
BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
DATA_DIR = BASE_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
templates = Jinja2Templates(directory=str(FRONTEND_DIR))

# 内存数据存储（实际项目中应该用数据库）
children_data = [
    {"id": 1, "name": "大宝", "grade": "高三"},
    {"id": 2, "name": "二宝", "grade": "学前"}
]

stats_data = {
    1: {"total_questions": 156, "correct_rate": "87%", "wrong_count": 20},
    2: {"total_questions": 32, "correct_rate": "94%", "wrong_count": 2}
}

knowledge_files = {}
upload_dir = DATA_DIR / "uploads"
upload_dir.mkdir(exist_ok=True)

# 2026年节日数据
holidays_2026 = {
    "春节": "2026年2月17日（农历正月初一）",
    "元宵节": "2026年3月3日（农历正月十五）",
    "清明节": "2026年4月5日",
    "劳动节": "2026年5月1日",
    "端午节": "2026年5月31日（农历五月初五）",
    "七夕节": "2026年8月19日（农历七月初七）",
    "中秋节": "2026年9月25日（农历八月十五）",
    "国庆节": "2026年10月1日",
    "重阳节": "2026年10月18日（农历九月初九）",
    "元旦": "2026年1月1日",
    "五一": "2026年5月1日",
    "十一": "2026年10月1日"
}

# 农历数据（简化版）
lunar_data = {
    "2026-05-10": "三月十四",
    "2026-05-11": "三月十五",
    "2026-05-12": "三月十六"
}

# 首页路由
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 静态文件重定向（兼容直接访问）
@app.get("/index.html")
async def index_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/styles.css")
async def styles_css():
    return FileResponse(str(FRONTEND_DIR / "styles.css"))

@app.get("/app.js")
async def app_js():
    return FileResponse(str(FRONTEND_DIR / "app.js"))

# 孩子管理API
@app.get("/api/children")
async def get_children():
    return {"children": children_data}

@app.put("/api/children/{child_id}")
async def update_child(child_id: int, request: Request):
    data = await request.json()
    for child in children_data:
        if child["id"] == child_id:
            child["name"] = data.get("name", child["name"])
            child["grade"] = data.get("grade", child["grade"])
            return {"success": True}
    raise HTTPException(status_code=404, detail="Child not found")

# 模型列表API
@app.get("/api/models/list")
async def get_models():
    # 模拟可用模型
    models_list = [
        {"name": "qwen2.5:7b-instruct-q4_K_M"},
        {"name": "llama2:7b-chat"},
        {"name": "gemma:7b"}
    ]
    return {"models": models_list}

# 诊断数据API
@app.get("/api/diagnosis")
async def get_diagnosis(child_id: int = 1):
    return stats_data.get(child_id, {"total_questions": 0, "correct_rate": "0%", "wrong_count": 0})

# 时间API
@app.get("/api/time")
async def get_time():
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M")
    weekday_str = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
    
    lunar_key = now.strftime("%Y-%m-%d")
    lunar_str = lunar_data.get(lunar_key, "农历日期")
    
    # 简单模拟节日判断
    holiday_str = ""
    if now.month == 5 and now.day == 1:
        holiday_str = "劳动节"
    
    return {
        "date": date_str,
        "time": time_str,
        "weekday": weekday_str,
        "lunar": lunar_str,
        "holiday": holiday_str
    }

@app.get("/api/time/countdown")
async def get_countdown(target: str):
    now = datetime.now()
    
    holiday_dates = {
        "春节": datetime(2026, 2, 17),
        "元宵": datetime(2026, 3, 3),
        "清明": datetime(2026, 4, 5),
        "劳动节": datetime(2026, 5, 1),
        "端午": datetime(2026, 5, 31),
        "七夕": datetime(2026, 8, 19),
        "中秋": datetime(2026, 9, 25),
        "国庆": datetime(2026, 10, 1),
        "元旦": datetime(2026, 1, 1),
        "除夕": datetime(2026, 2, 16)
    }
    
    if target in holiday_dates:
        target_date = holiday_dates[target]
        delta = target_date - now
        
        if delta.days > 0:
            return {"message": f"距离{target}还有 {delta.days} 天"}
        elif delta.days == 0:
            return {"message": f"今天就是{target}！🎉"}
        else:
            return {"message": f"{target}已经过去 {abs(delta.days)} 天了"}
    
    return {"message": ""}

# Ollama聊天API（模拟）
@app.post("/api/ollama/chat")
async def ollama_chat(request: Request):
    data = await request.json()
    model = data.get("model", "qwen2.5:7b-instruct-q4_K_M")
    messages = data.get("messages", [])
    
    user_message = ""
    for msg in messages:
        if msg["role"] == "user":
            user_message = msg["content"]
    
    # 模拟响应
    async def generate_response():
        responses = [
            "你好！我是小熊老师，很高兴能帮助你！",
            "这个问题很有趣，让我来帮你解答。",
            "学习是一个渐进的过程，让我们一起努力！",
            "这个知识点很重要，让我详细解释一下..."
        ]
        
        response_text = random.choice(responses)
        
        # 模拟流式输出
        for char in response_text:
            chunk = json.dumps({"message": {"content": char}}, ensure_ascii=False)
            yield f"{chunk}\n"
            await asyncio.sleep(0.05)
    
    return StreamingResponse(generate_response(), media_type="application/x-ndjson")

# 考试生成API
@app.post("/api/exam/generate")
async def generate_exam(request: Request):
    data = await request.json()
    grade = data.get("grade", "小学一年级")
    subject = data.get("subject", "数学")
    count = data.get("count", 10)
    
    # 生成模拟题目
    questions = []
    for i in range(count):
        if subject == "数学":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(["+", "-"])
            answer = a + b if op == "+" else a - b
            questions.append({
                "id": i + 1,
                "type": "口算题",
                "question": f"{a} {op} {b} = ?",
                "answer": str(answer),
                "explanation": f"{a} {op} {b} = {answer}"
            })
        elif subject == "语文":
            questions.append({
                "id": i + 1,
                "type": "填空题",
                "question": "春眠不觉晓，处处闻啼___。",
                "answer": "鸟",
                "explanation": "出自孟浩然《春晓》"
            })
    
    return {"success": True, "questions": questions}

# 照片上传API
@app.post("/api/photo")
async def upload_photo(photo: UploadFile = File(...), child_id: int = 1):
    # 模拟处理
    content = await photo.read()
    return {
        "success": True,
        "result": "识别到的作业内容...\n（模拟数据）\n1. 1+1=?\n2. 2+2=?"
    }

@app.post("/api/photo/grade")
async def grade_photo(request: Request):
    data = await request.json()
    extracted = data.get("extracted", "")
    
    # 模拟批改
    return {
        "success": True,
        "grade": {
            "correct": 8,
            "total": 10,
            "wrong_questions": [
                {
                    "question": "1. 3+4=?",
                    "student_answer": "6",
                    "correct_answer": "7"
                }
            ],
            "diagnosis": "整体掌握不错，但个别计算需要再仔细一点。"
        }
    }

# 学习计划API
@app.post("/api/plan/generate")
async def generate_plan(request: Request):
    data = await request.json()
    
    return {
        "success": True,
        "plan": {
            "goal": "掌握本周的数学基础知识",
            "daily": [
                "周一：复习加法运算，做10道练习题",
                "周二：复习减法运算，做10道练习题",
                "周三：混合运算练习",
                "周四：错题复习",
                "周五：综合测试",
                "周六：休息和阅读",
                "周日：预习下周内容"
            ]
        }
    }

# 知识库API
@app.get("/api/kb/list")
async def list_kb(child_id: int = 1):
    files_list = []
    if child_id in knowledge_files:
        files_list = knowledge_files[child_id]
    return {"files": files_list}

# 文件上传
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), child_id: int = 1):
    file_location = upload_dir / file.filename
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
    
    if child_id not in knowledge_files:
        knowledge_files[child_id] = []
    
    knowledge_files[child_id].append({
        "filename": file.filename,
        "text_len": len(content),
        "uploaded_at": datetime.now().isoformat()
    })
    
    return {"message": "上传成功"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
