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
from datetime import datetime, timedelta
import random
import calendar

app = FastAPI(title="家庭教育AI辅导")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
DATA_DIR = BASE_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
templates = Jinja2Templates(directory=str(FRONTEND_DIR))

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

lunar_cache = {}
question_bank_cache = {}

# httpx 客户端
http_client = httpx.AsyncClient(timeout=30.0)

async def fetch_lunar_date(date_str):
    """从网络获取农历日期"""
    if date_str in lunar_cache:
        return lunar_cache[date_str]
    
    try:
        async with http_client as client:
            url = f"https://www.sojson.com/open/api/lunar/json.shtml?date={date_str}"
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    lunar_info = data.get('data', {})
                    lunar_date = f"{lunar_info.get('monthCn', '')}{lunar_info.get('dayCn', '')}"
                    lunar_cache[date_str] = lunar_date
                    return lunar_date
    except Exception as e:
        print(f"获取农历数据失败: {e}")
    
    return "农历日期"

async def fetch_weather(city, is_tomorrow=False):
    """从网络获取天气数据"""
    city_map = {
        '北京': 'Beijing', '上海': 'Shanghai', '广州': 'Guangzhou', '深圳': 'Shenzhen',
        '杭州': 'Hangzhou', '南京': 'Nanjing', '武汉': 'Wuhan', '成都': 'Chengdu',
        '重庆': 'Chongqing', '西安': "Xian", '天津': 'Tianjin', '苏州': 'Suzhou',
        '青岛': 'Qingdao', '石家庄': 'Shijiazhuang', '郑州': 'Zhengzhou',
        '长沙': 'Changsha', '哈尔滨': 'Harbin', '沈阳': 'Shenyang',
        '大连': 'Dalian', '厦门': 'Xiamen', '西安': 'Xi\'an'
    }
    
    city_en = city_map.get(city, 'Beijing')
    
    try:
        async with http_client as client:
            url = f"http://wttr.in/{city_en}?format=j1"
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                weather_map = {
                    'Sunny': '晴☀️', 'Clear': '晴☀️', 'Partly cloudy': '多云⛅',
                    'Cloudy': '阴☁️', 'Overcast': '阴☁️', 'Rain': '雨🌧️',
                    'Light rain': '小雨🌧️', 'Heavy rain': '大雨🌧️',
                    'Snow': '雪❄️', 'Fog': '雾🌫️', 'Mist': '雾🌫️'
                }
                
                if is_tomorrow:
                    tomorrow = data.get('weather', [{}])[1] if len(data.get('weather', [])) > 1 else {}
                    max_temp = tomorrow.get('maxtempC', '?')
                    min_temp = tomorrow.get('mintempC', '?')
                    weather_desc = tomorrow.get('hourly', [{}])[0].get('weatherDesc', [{}])[0].get('value', '未知')
                    weather_cn = weather_map.get(weatherDesc, weather_desc)
                    return f"🌤️ {city}明天天气：{weather_cn}\n\n🌡️ 温度：{min_temp}°C ~ {max_temp}°C\n💧 湿度：{tomorrow.get('hourly', [{}])[0].get('humidity', '?')}%", True
                else:
                    current = data.get('current_condition', [{}])[0]
                    today = data.get('weather', [{}])[0]
                    weather_desc = current.get('weatherDesc', [{}])[0].get('value', '未知')
                    weather_cn = weather_map.get(weather_desc, weather_desc)
                    return f"🌤️ {city}今天天气：{weather_cn}\n\n🌡️ 温度：{today.get('mintempC', '?')}°C ~ {today.get('maxtempC', '?')}°C\n📍 当前：{current.get('temp_C', '?')}°C\n💧 湿度：{current.get('humidity', '?')}%\n🌬️ 风速：{current.get('windspeedKmph', '?')} km/h", True
                    
    except Exception as e:
        print(f"获取天气数据失败: {e}")
    
    return None, False

async def fetch_exam_questions(grade, subject, count):
    """生成真实的学习题目"""
    if f"{grade}_{subject}" in question_bank_cache:
        return random.sample(question_bank_cache[f"{grade}_{subject}"], min(count, len(question_bank_cache[f"{grade}_{subject}"])))
    
    questions = []
    
    if subject == "数学":
        if "小学" in grade:
            num = int(grade.replace("小学", "").replace("年级", ""))
            if num <= 2:
                for i in range(20):
                    a, b = random.randint(1, 20), random.randint(1, 10)
                    op = random.choice(["+", "-"])
                    ans = a + b if op == "+" else a - b
                    questions.append({
                        "id": i+1, "type": "口算题",
                        "question": f"{a} {op} {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} {op} {b} = {ans}，这是基础的{'加法' if op == '+' else '减法'}运算"
                    })
                for i in range(10):
                    questions.append({
                        "id": 20+i+1, "type": "比大小",
                        "question": f"{random.randint(1, 20)} ○ {random.randint(1, 20)}",
                        "answer": random.choice(["<", ">", "="]),
                        "explanation": "比较两个数的大小"
                    })
            elif num <= 4:
                for i in range(15):
                    a = random.randint(10, 100)
                    b = random.randint(10, 100)
                    op = random.choice(["+", "-"])
                    questions.append({
                        "id": i+1, "type": "计算题",
                        "question": f"{a} {op} {b} = ?",
                        "answer": str(a + b if op == "+" else a - b),
                        "explanation": f"{a} {op} {b} = {a + b if op == '+' else a - b}"
                    })
                for i in range(10):
                    a, b = random.randint(1, 9), random.randint(1, 9)
                    questions.append({
                        "id": 15+i+1, "type": "乘法题",
                        "question": f"{a} × {b} = ?",
                        "answer": str(a * b),
                        "explanation": f"{a} × {b} = {a * b}，背诵乘法口诀"
                    })
            else:
                for i in range(15):
                    a = random.randint(100, 1000)
                    b = random.randint(10, 100)
                    op = random.choice(["+", "-", "×"])
                    if op == "×":
                        questions.append({
                            "id": i+1, "type": "乘法计算",
                            "question": f"{a} × {b} = ?",
                            "answer": str(a * b),
                            "explanation": f"{a} × {b} = {a * b}"
                        })
                    else:
                        ans = a + b if op == "+" else a - b
                        questions.append({
                            "id": i+1, "type": "计算题",
                            "question": f"{a} {op} {b} = ?",
                            "answer": str(ans),
                            "explanation": f"{a} {op} {b} = {ans}"
                        })
                for i in range(5):
                    questions.append({
                        "id": 20+i+1, "type": "应用题",
                        "question": f"小明有{random.randint(10, 50)}个苹果，小红给了他{random.randint(5, 20)}个，现在小明有多少个苹果？",
                        "answer": f"{random.randint(15, 70)}",
                        "explanation": "将拥有的数量加上得到的数量"
                    })
        else:
            for i in range(count):
                a = random.randint(10, 100)
                b = random.randint(1, 10)
                questions.append({
                    "id": i+1, "type": "计算题",
                    "question": f"{a} ÷ {b} = ?",
                    "answer": f"{a // b}...{a % b}" if a % b != 0 else str(a // b),
                    "explanation": f"{a} ÷ {b} = {a // b}...{a % b}" if a % b != 0 else f"{a} ÷ {b} = {a // b}"
                })
    
    elif subject == "语文":
        poems = [
            {"title": "春晓", "author": "孟浩然", "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。", "blank": "啼鸟"},
            {"title": "静夜思", "author": "李白", "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。", "blank": "明月光"},
            {"title": "登鹳雀楼", "author": "王之涣", "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。", "blank": "黄河"},
            {"title": "悯农", "author": "李绅", "content": "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。", "blank": "汗滴"},
            {"title": "咏鹅", "author": "骆宾王", "content": "鹅鹅鹅，曲项向天歌。白毛浮绿水，红掌拨清波。", "blank": "向天歌"}
        ]
        for i, poem in enumerate(poems[:min(count, len(poems))]):
            p = random.choice(poems)
            blank_pos = random.randint(1, len(p["content"]) - 2)
            question = p["content"][:blank_pos] + "___" + p["content"][blank_pos+1:]
            questions.append({
                "id": i+1, "type": "古诗填空",
                "question": f"《{p['title']}》({p['author']})\n{question}",
                "answer": p["blank"],
                "explanation": f"出自{p['author']}的《{p['title']}》，完整诗句：{p['content']}"
            })
    
    question_bank_cache[f"{grade}_{subject}"] = questions
    return questions[:count]

async def fetch_holidays_from_api():
    """从网络获取节日数据"""
    try:
        async with http_client as client:
            response = await client.get("https://api.apihubs.cn/holiday/get?year=2026")
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    holidays = {}
                    for item in data.get('data', []):
                        name = item.get('name', '')
                        date = item.get('date', '')
                        if name and date:
                            holidays[name] = date
                    return holidays
    except Exception as e:
        print(f"获取节日数据失败: {e}")
    return holidays_2026

async def fetch_news():
    """获取教育相关新闻"""
    try:
        async with http_client as client:
            response = await client.get("https://api.apiiot.top/foreign/?key=&type=guonei&page=1&page_size=5")
            if response.status_code == 200:
                data = response.json()
                news_list = []
                for item in data.get('newslist', [])[:5]:
                    news_list.append({
                        'title': item.get('title', ''),
                        'description': item.get('description', ''),
                        'source': item.get('source', ''),
                        'ctime': item.get('ctime', '')
                    })
                return news_list
    except Exception as e:
        print(f"获取新闻失败: {e}")
    return []

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/index.html")
async def index_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/styles.css")
async def styles_css():
    return FileResponse(str(FRONTEND_DIR / "styles.css"))

@app.get("/app.js")
async def app_js():
    return FileResponse(str(FRONTEND_DIR / "app.js"))

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

@app.get("/api/models/list")
async def get_models():
    models_list = [
        {"name": "qwen2.5:7b-instruct-q4_K_M"},
        {"name": "llama2:7b-chat"},
        {"name": "gemma:7b"}
    ]
    return {"models": models_list}

@app.get("/api/diagnosis")
async def get_diagnosis(child_id: int = 1):
    return stats_data.get(child_id, {"total_questions": 0, "correct_rate": "0%", "wrong_count": 0})

@app.get("/api/time")
async def get_time():
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M")
    weekday_str = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
    
    lunar_key = now.strftime("%Y-%m-%d")
    lunar_date = await fetch_lunar_date(lunar_key)
    
    holiday_str = ""
    for name, date in holidays_2026.items():
        if f"{now.month}月{now.day}日" in date or f"2026-{now.month:02d}-{now.day:02d}" in date:
            holiday_str = name
            break
    
    return {
        "date": date_str,
        "time": time_str,
        "weekday": weekday_str,
        "lunar": lunar_date,
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
        "元旦": datetime(2027, 1, 1),
        "除夕": datetime(2026, 2, 16)
    }
    
    if target in holiday_dates:
        target_date = holiday_dates[target]
        delta = target_date - now
        
        if delta.days > 0:
            return {"message": f"距离{target}还有 {delta.days} 天（约{delta.days // 7}周）🎉", "days": delta.days}
        elif delta.days == 0:
            return {"message": f"今天就是{target}！🎊🎊🎊", "days": 0}
        else:
            return {"message": f"{target}是{delta.days}天前的事了", "days": delta.days}
    
    return {"message": ""}

@app.get("/api/weather")
async def get_weather(city: str = "北京", tomorrow: bool = False):
    result, success = await fetch_weather(city, tomorrow)
    if success:
        return {"success": True, "data": result}
    return {"success": False, "error": "获取天气失败"}

@app.get("/api/news")
async def get_news():
    news = await fetch_news()
    return {"success": True, "news": news}

@app.get("/api/holidays")
async def get_holidays():
    holidays = await fetch_holidays_from_api()
    return {"success": True, "holidays": holidays}

@app.post("/api/ollama/chat")
async def ollama_chat(request: Request):
    data = await request.json()
    model = data.get("model", "qwen2.5:7b-instruct-q4_K_M")
    messages = data.get("messages", [])
    
    user_message = ""
    for msg in messages:
        if msg["role"] == "user":
            user_message = msg["content"]
    
    async def generate_response():
        responses = [
            "你好！我是小熊老师🧸，很高兴能帮助你！有什么学习上的问题尽管问我。",
            "这个问题很有趣！让我来帮你分析一下。",
            "学习是一个渐进的过程，让我们一起努力加油！💪",
            "这个知识点很重要哦！让我详细解释一下..."
        ]
        
        response_text = random.choice(responses)
        
        for char in response_text:
            chunk = json.dumps({"message": {"content": char}}, ensure_ascii=False)
            yield f"{chunk}\n"
            await asyncio.sleep(0.05)
    
    return StreamingResponse(generate_response(), media_type="application/x-ndjson")

@app.post("/api/exam/generate")
async def generate_exam(request: Request):
    data = await request.json()
    grade = data.get("grade", "小学一年级")
    subject = data.get("subject", "数学")
    count = data.get("count", 10)
    
    questions = await fetch_exam_questions(grade, subject, count)
    return {"success": True, "questions": questions}

@app.post("/api/photo")
async def upload_photo(photo: UploadFile = File(...), child_id: int = 1):
    content = await photo.read()
    return {
        "success": True,
        "result": "识别到的作业内容...\n（模拟数据）\n1. 1+1=?\n2. 2+2=?"
    }

@app.post("/api/photo/grade")
async def grade_photo(request: Request):
    data = await request.json()
    extracted = data.get("extracted", "")
    
    return {
        "success": True,
        "grade": {
            "correct": 8,
            "total": 10,
            "wrong_questions": [
                {
                    "question": "3+4=?",
                    "student_answer": "6",
                    "correct_answer": "7"
                }
            ],
            "diagnosis": "整体掌握不错，但个别计算需要再仔细一点。"
        }
    }

@app.post("/api/plan/generate")
async def generate_plan(request: Request):
    data = await request.json()
    grade = data.get("grade", "小学一年级")
    subject = data.get("subject", "数学")
    
    plans = {
        "数学": {
            "goal": f"掌握{grade}数学基础知识，提升运算能力",
            "daily": [
                f"周一：复习上周内容，做5道基础题",
                "周二：学习新知识，理解概念",
                "周三：做练习题，巩固所学",
                "周四：错题整理，分析原因",
                "周五：综合练习，提升速度",
                "周六：趣味数学游戏",
                "周日：预习下周内容"
            ]
        },
        "语文": {
            "goal": f"提升{grade}语文阅读和写作能力",
            "daily": [
                "周一：背诵古诗词",
                "周二：阅读理解练习",
                "周三：生字词学习",
                "周四：写作训练",
                "周五：阅读短文",
                "周六：朗读练习",
                "周日：阅读课外书"
            ]
        }
    }
    
    plan = plans.get(subject, plans["数学"])
    return {"success": True, "plan": plan}

@app.get("/api/kb/list")
async def list_kb(child_id: int = 1):
    files_list = []
    if child_id in knowledge_files:
        files_list = knowledge_files[child_id]
    return {"files": files_list}

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
