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
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
import calendar
from collections import defaultdict
from database import db

app = FastAPI(title="家庭教育AI辅导系统")

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

# ============ 数据存储 ============

children_data = [
    {"id": 1, "name": "大宝", "grade": "高三", "avatar": "🎓", "points": 1250, "level": 8, "streak": 15},
    {"id": 2, "name": "二宝", "grade": "学前", "avatar": "🧒", "points": 580, "level": 4, "streak": 7}
]

# 学习进度数据
learning_progress = defaultdict(lambda: {
    "total_questions": 0,
    "correct_questions": 0,
    "study_time": 0,
    "completed_topics": [],
    "weak_points": [],
    "strong_points": [],
    "daily_record": [],
    "achievements": []
})

# 错题本
wrong_questions = defaultdict(list)

# 知识库
knowledge_base = {}

# 成就系统
achievements = {
    "first_question": {"name": "初次答题", "desc": "完成第一道题", "icon": "🌟", "points": 10},
    "streak_7": {"name": "连续7天", "desc": "学习连续打卡7天", "icon": "🔥", "points": 50},
    "streak_30": {"name": "坚持一个月", "desc": "学习连续打卡30天", "icon": "💎", "points": 200},
    "math_master": {"name": "数学大师", "desc": "数学正确率达到90%", "icon": "🧮", "points": 100},
    "poem_master": {"name": "诗词达人", "desc": "背诵10首古诗", "icon": "📜", "points": 80},
    "speed_demon": {"name": "速算达人", "desc": "10秒内完成口算", "icon": "⚡", "points": 30},
    "perfect_day": {"name": "完美一天", "desc": "一天内完成所有任务", "icon": "👑", "points": 100},
    "bookworm": {"name": "小书虫", "desc": "阅读10篇知识", "icon": "📚", "points": 60},
    "parent_helper": {"name": "家长小助手", "desc": "帮助家长完成任务", "icon": "🤝", "points": 40},
    "explorer": {"name": "知识探险家", "desc": "学习5个不同主题", "icon": "🗺️", "points": 50}
}

# 学习主题库
topics = {
    "数学": {
        "小学一年级": ["数数与比大小", "10以内加减法", "认识图形", "分类与顺序", "位置与方向"],
        "小学二年级": ["100以内加减法", "乘法入门", "认识时间", "认识人民币", "简单统计"],
        "小学三年级": ["万以内加减法", "乘法竖式", "除法入门", "分数初步", "面积周长"],
        "小学四年级": ["大数运算", "公顷和平方千米", "角的度量", "平行四边形", "条形统计图"],
        "小学五年级": ["小数运算", "因数和倍数", "分数加减法", "折线统计图", "植树问题"],
        "小学六年级": ["分数乘法除法", "比和比例", "百分数", "圆与扇形", "比例尺"],
        "初一": ["有理数运算", "整式加减", "一元一次方程", "几何图形", "数据统计"],
        "初二": ["全等三角形", "轴对称", "整式乘法", "分式", "二次根式"],
        "初三": ["一元二次方程", "二次函数", "圆", "相似三角形", "锐角三角函数"],
        "高一": ["集合与函数", "指数与对数", "三角函数", "平面向量", "数列"],
        "高二": ["导数", "概率与统计", "排列组合", "复数", "推理与证明"],
        "高三": ["函数综合", "解析几何", "立体几何", "概率统计", "导数及其应用"]
    },
    "语文": {
        "小学一年级": ["拼音基础", "生字学习", "简单词语", "朗读训练", "看图说话"],
        "小学二年级": ["部首查字法", "词语搭配", "简单句子", "古诗背诵", "阅读理解"],
        "小学三年级": ["写作入门", "段落结构", "修辞手法", "古诗词", "课外阅读"],
        "小学四年级": ["文章结构", "说明文阅读", "文言文启蒙", "写作技巧", "名著导读"],
        "小学五年级": ["说明方法", "议论基础", "文言文学习", "写作提升", "文学常识"],
        "小学六年级": ["阅读理解", "写作技巧", "文言文进阶", "诗词鉴赏", "名著阅读"],
        "初一": ["记叙文阅读", "写作训练", "文言文", "诗词鉴赏", "综合性学习"],
        "初二": ["说明文进阶", "议论文入门", "文言文", "现代诗歌", "名著导读"],
        "初三": ["阅读综合", "写作提升", "文言文", "诗词", "名著复习"],
        "高一": ["现代文阅读", "文言文", "诗词鉴赏", "写作", "文学常识"],
        "高二": ["阅读深化", "写作创新", "文言文", "诗词", "文化传承"],
        "高三": ["应试阅读", "写作强化", "文言文", "诗词", "总复习"]
    },
    "英语": {
        "小学三年级": ["字母学习", "基础单词", "简单句子", "日常用语", "歌曲学英语"],
        "小学四年级": ["单词积累", "基本时态", "对话练习", "阅读入门", "书写规范"],
        "小学五年级": ["词汇扩展", "现在进行时", "阅读理解", "写作基础", "口语练习"],
        "小学六年级": ["小升初复习", "综合运用", "阅读提升", "写作", "小升初备考"],
        "初一": ["音标学习", "初一上册", "初一下册", "语法入门", "听说训练"],
        "初二": ["初二上册", "初二下册", "语法进阶", "阅读提升", "写作"],
        "初三": ["中考复习", "语法系统", "阅读强化", "写作提升", "中考备考"],
        "高一": ["必修一", "必修二", "语法深化", "阅读拓展", "写作训练"],
        "高二": ["选择性必修", "语法系统", "阅读提升", "写作", "素养培养"],
        "高三": ["高考复习", "语法系统", "阅读强化", "写作", "高考备考"]
    }
}

# 古诗词库
poems_db = [
    {"title": "春晓", "author": "孟浩然", "dynasty": "唐", "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。", "category": "写景", "difficulty": 1},
    {"title": "静夜思", "author": "李白", "dynasty": "唐", "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。", "category": "思乡", "difficulty": 1},
    {"title": "登鹳雀楼", "author": "王之涣", "dynasty": "唐", "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。", "category": "哲理", "difficulty": 1},
    {"title": "悯农", "author": "李绅", "dynasty": "唐", "content": "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。", "category": "咏物", "difficulty": 1},
    {"title": "咏鹅", "author": "骆宾王", "dynasty": "唐", "content": "鹅鹅鹅，曲项向天歌。白毛浮绿水，红掌拨清波。", "category": "咏物", "difficulty": 1},
    {"title": "江雪", "author": "柳宗元", "dynasty": "唐", "content": "千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。", "category": "写景", "difficulty": 2},
    {"title": "寻隐者不遇", "author": "贾岛", "dynasty": "唐", "content": "松下问童子，言师采药去。只在此山中，云深不知处。", "category": "叙事", "difficulty": 2},
    {"title": "枫桥夜泊", "author": "张继", "dynasty": "唐", "content": "月落乌啼霜满天，江枫渔火对愁眠。姑苏城外寒山寺，夜半钟声到客船。", "category": "羁旅", "difficulty": 2},
    {"title": "游子吟", "author": "孟郊", "dynasty": "唐", "content": "慈母手中线，游子身上衣。临行密密缝，意恐迟迟归。谁言寸草心，报得三春晖。", "category": "亲情", "difficulty": 2},
    {"title": "望庐山瀑布", "author": "李白", "dynasty": "唐", "content": "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。", "category": "写景", "difficulty": 2},
    {"title": "绝句", "author": "杜甫", "dynasty": "唐", "content": "两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。", "category": "写景", "difficulty": 2},
    {"title": "清明", "author": "杜牧", "dynasty": "唐", "content": "清明时节雨纷纷，路上行人欲断魂。借问酒家何处有，牧童遥指杏花村。", "category": "写景", "difficulty": 2},
    {"title": "黄鹤楼送孟浩然之广陵", "author": "李白", "dynasty": "唐", "content": "故人西辞黄鹤楼，烟花三月下扬州。孤帆远影碧空尽，唯见长江天际流。", "category": "送别", "difficulty": 3},
    {"title": "出塞", "author": "王昌龄", "dynasty": "唐", "content": "秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度阴山。", "category": "边塞", "difficulty": 3},
    {"title": "回乡偶书", "author": "贺知章", "dynasty": "唐", "content": "少小离家老大回，乡音无改鬓毛衰。儿童相见不相识，笑问客从何处来。", "category": "思乡", "difficulty": 2},
]

# 知识百科
knowledge_articles = [
    {"id": 1, "title": "为什么先有乘法后有除法？", "category": "数学思维", "summary": "乘法是加法的简便运算，除法是乘法的逆运算。", "content": "乘法本质上是多个相同加数的加法，比如3×4就是4个3相加。而除法是乘法的逆运算，用于把一个数平均分成若干份，或者求一个数里包含多少个另一个数。", "tags": ["数学", "思维"], "difficulty": 2},
    {"id": 2, "title": "古代诗人为什么喜欢写月？", "category": "诗词文化", "summary": "月亮在中国文化中象征思念、团圆和美好。", "content": "在中国传统文化中，月亮具有丰富的象征意义：1.象征思念和团圆 2.象征高洁品格 3.作为时间参照 4.引发诗人灵感。因此诗人们经常借月抒情，表达思乡、怀人、感慨时光等情感。", "tags": ["语文", "文化"], "difficulty": 2},
    {"id": 3, "title": "英语为什么要学语法？", "category": "学习方法", "summary": "语法是语言的规则，帮助我们正确表达。", "content": "语法是组织语言的规则系统。学习语法的原因：1.帮助正确表达思想 2.提高理解和沟通效率 3.为高级语言能力打基础 4.考试需要。但语法要在大量实践中自然掌握。", "tags": ["英语", "学习"], "difficulty": 2},
    {"id": 4, "title": "为什么0不能作除数？", "category": "数学原理", "summary": "因为会导致逻辑矛盾和数学系统崩溃。", "content": "如果a÷0=b，那么b×0=a，无论b是多少，b×0都等于0，无法得到a（除非a也是0）。更严重的是，0÷0可以是任何数，这会导致数学逻辑混乱。所以数学规定0不能作除数。", "tags": ["数学", "原理"], "difficulty": 3},
    {"id": 5, "title": "如何培养阅读习惯？", "category": "学习习惯", "summary": "从兴趣出发，每天固定时间阅读。", "content": "培养阅读习惯的方法：1.从感兴趣的书开始 2.设定每天固定的阅读时间 3.创造舒适的阅读环境 4.做好读书笔记 5.与他人讨论书中内容 6.参加读书会。循序渐进，养成习惯。", "tags": ["方法", "习惯"], "difficulty": 1},
]

# 题目缓存
question_cache = {}
question_bank = defaultdict(list)

# HTTP客户端
http_client = httpx.AsyncClient(timeout=30.0)

# 缓存
lunar_cache = {}

# ============ 辅助函数 ============

async def fetch_lunar_date(date_str):
    """获取农历日期"""
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
    except Exception:
        pass
    
    return "农历日期"

async def fetch_weather(city, is_tomorrow=False):
    """获取天气数据"""
    city_map = {
        '北京': 'Beijing', '上海': 'Shanghai', '广州': 'Guangzhou', '深圳': 'Shenzhen',
        '杭州': 'Hangzhou', '南京': 'Nanjing', '武汉': 'Wuhan', '成都': 'Chengdu',
        '重庆': 'Chongqing', '西安': "Xian", '天津': 'Tianjin', '苏州': 'Suzhou',
        '青岛': 'Qingdao', '石家庄': 'Shijiazhuang', '郑州': 'Zhengzhou',
        '长沙': 'Changsha', '哈尔滨': 'Harbin', '沈阳': 'Shenyang'
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
    except Exception:
        pass
    
    return None, False

def generate_math_questions(grade: str, count: int) -> List[Dict]:
    """生成数学题目"""
    questions = []
    
    if "小学" in grade:
        num = int(grade.replace("小学", "").replace("年级", ""))
        
        if num == 1:
            for i in range(count):
                a, b = random.randint(1, 10), random.randint(1, 10)
                if a >= b:
                    op = "+"
                    ans = a + b
                else:
                    op = "-"
                    ans = a - b
                    a, b = b, a
                
                q_type = random.choice(["口算题", "比大小", "填空题"])
                if q_type == "口算题":
                    questions.append({
                        "id": i+1, "type": q_type, "topic": "10以内加减法",
                        "question": f"{a} {op} {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} {op} {b} = {ans}，这是基础的{'加法' if op == '+' else '减法'}运算",
                        "difficulty": 1
                    })
                elif q_type == "比大小":
                    x, y = random.randint(1, 10), random.randint(1, 10)
                    ans = "<" if x < y else ">" if x > y else "="
                    questions.append({
                        "id": i+1, "type": q_type, "topic": "比大小",
                        "question": f"{x} ○ {y}，圆圈里填 >、< 或 =",
                        "answer": ans,
                        "explanation": f"{x} {'<' if ans == '<' else '>' if ans == '>' else '='} {y}",
                        "difficulty": 1
                    })
                else:
                    a, b = random.randint(1, 10), random.randint(1, 10)
                    if a >= b:
                        ans = a - b
                        questions.append({
                            "id": i+1, "type": q_type, "topic": "10以内减法",
                            "question": f"{a} - {b} = ?",
                            "answer": str(ans),
                            "explanation": f"{a} - {b} = {ans}",
                            "difficulty": 1
                        })
        
        elif num == 2:
            for i in range(count):
                if i % 2 == 0:
                    a, b = random.randint(10, 99), random.randint(10, 99)
                    op = random.choice(["+", "-"])
                    ans = a + b if op == "+" else a - b
                    questions.append({
                        "id": i+1, "type": "计算题", "topic": "100以内加减法",
                        "question": f"{a} {op} {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} {op} {b} = {ans}",
                        "difficulty": 2
                    })
                else:
                    a, b = random.randint(1, 9), random.randint(1, 9)
                    ans = a * b
                    questions.append({
                        "id": i+1, "type": "乘法题", "topic": "乘法入门",
                        "question": f"{a} × {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} × {b} = {ans}，背诵乘法口诀",
                        "difficulty": 2
                    })
        
        elif num == 3:
            for i in range(count):
                if i % 3 == 0:
                    a = random.randint(100, 999)
                    b = random.randint(10, 99)
                    op = random.choice(["+", "-"])
                    ans = a + b if op == "+" else a - b
                    questions.append({
                        "id": i+1, "type": "计算题", "topic": "万以内加减法",
                        "question": f"{a} {op} {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} {op} {b} = {ans}",
                        "difficulty": 3
                    })
                elif i % 3 == 1:
                    a, b = random.randint(10, 99), random.randint(1, 9)
                    ans = a * b
                    questions.append({
                        "id": i+1, "type": "乘法竖式", "topic": "乘法竖式",
                        "question": f"{a} × {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} × {b} = {ans}",
                        "difficulty": 3
                    })
                else:
                    a = random.randint(20, 99)
                    b = random.randint(2, 9)
                    ans = a // b
                    rem = a % b
                    questions.append({
                        "id": i+1, "type": "除法题", "topic": "除法入门",
                        "question": f"{a} ÷ {b} = ? ... ?",
                        "answer": f"{ans}...{rem}" if rem else str(ans),
                        "explanation": f"{a} ÷ {b} = {ans}...{rem}" if rem else f"{a} ÷ {b} = {ans}",
                        "difficulty": 3
                    })
        
        else:
            for i in range(count):
                if i % 4 == 0:
                    a = random.randint(100, 9999)
                    b = random.randint(100, 999)
                    op = random.choice(["+", "-"])
                    ans = a + b if op == "+" else a - b
                    questions.append({
                        "id": i+1, "type": "计算题", "topic": "大数运算",
                        "question": f"{a} {op} {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} {op} {b} = {ans}",
                        "difficulty": 4
                    })
                elif i % 4 == 1:
                    a, b = random.randint(10, 999), random.randint(10, 99)
                    ans = a * b
                    questions.append({
                        "id": i+1, "type": "计算题", "topic": "乘法运算",
                        "question": f"{a} × {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} × {b} = {ans}",
                        "difficulty": 4
                    })
                elif i % 4 == 2:
                    a = random.randint(100, 999)
                    b = random.randint(2, 9)
                    ans = a // b
                    rem = a % b
                    questions.append({
                        "id": i+1, "type": "计算题", "topic": "除法运算",
                        "question": f"{a} ÷ {b} = ? ... ?",
                        "answer": f"{ans}...{rem}" if rem else str(ans),
                        "explanation": f"{a} ÷ {b} = {ans}...{rem}" if rem else f"{a} ÷ {b} = {ans}",
                        "difficulty": 4
                    })
                else:
                    a, b = random.randint(1, 100), random.randint(1, 100)
                    c = random.randint(1, 50)
                    questions.append({
                        "id": i+1, "type": "应用题", "topic": "实际问题",
                        "question": f"小明有{a}元，买了{b}元的东西，又捡到{c}元，现在有多少元？",
                        "answer": str(a - b + c),
                        "explanation": f"先算花掉后：{a} - {b} = {a-b}，再加捡到的：{a-b} + {c} = {a-b+c}",
                        "difficulty": 4
                    })
    
    elif "初一" in grade:
        for i in range(count):
            if i % 2 == 0:
                a = random.randint(-99, 99)
                b = random.randint(1, 20)
                op = random.choice(["+", "-"])
                if a >= 0:
                    ans = a + b if op == "+" else a - b
                    questions.append({
                        "id": i+1, "type": "计算题", "topic": "有理数运算",
                        "question": f"{a} {op} {b} = ?",
                        "answer": str(ans),
                        "explanation": f"{a} {op} {b} = {ans}",
                        "difficulty": 3
                    })
            else:
                x = random.randint(1, 10)
                ans_val = random.randint(1, 50)
                questions.append({
                    "id": i+1, "type": "方程题", "topic": "一元一次方程",
                    "question": f"x + {x} = {ans_val + x}，求x",
                    "answer": str(ans_val),
                    "explanation": f"移项得 x = {ans_val + x} - {x} = {ans_val}",
                    "difficulty": 3
                })
    
    elif "高一" in grade or "高二" in grade or "高三" in grade:
        for i in range(count):
            if i % 3 == 0:
                a = random.randint(1, 10)
                b = random.randint(1, 10)
                questions.append({
                    "id": i+1, "type": "计算题", "topic": "指数运算",
                    "question": f"{a}^{b} = ?",
                    "answer": str(a ** b),
                    "explanation": f"{a}^{b} = {a ** b}",
                    "difficulty": 4
                })
            elif i % 3 == 1:
                a = random.randint(1, 10)
                questions.append({
                    "id": i+1, "type": "计算题", "topic": "对数运算",
                    "question": f"log₂({a ** random.randint(1,4)}) = ?",
                    "answer": str(random.randint(1, 4) * int(round(a**0.5)) if a > 1 else 1),
                    "explanation": "根据对数定义",
                    "difficulty": 5
                })
            else:
                questions.append({
                    "id": i+1, "type": "综合题", "topic": "函数",
                    "question": f"已知f(x) = {random.randint(1,5)}x + {random.randint(1,10)}，求f({random.randint(1,10)})",
                    "answer": str(random.randint(1, 100)),
                    "explanation": "代入计算即可",
                    "difficulty": 4
                })
    
    return questions[:count]

def generate_chinese_questions(grade: str, count: int) -> List[Dict]:
    """生成语文题目"""
    questions = []
    
    if "小学" in grade:
        num = int(grade.replace("小学", "").replace("年级", ""))
        
        for i in range(count):
            if num <= 2:
                p = random.choice([p for p in poems_db if p['difficulty'] <= 1])
                blank_pos = random.randint(2, len(p["content"]) - 2)
                q_text = p["content"][:blank_pos] + "___" + p["content"][blank_pos+1:]
                questions.append({
                    "id": i+1, "type": "古诗填空", "topic": "古诗背诵",
                    "question": f"《{p['title']}》({p['author']})\n{q_text}",
                    "answer": p["content"][blank_pos],
                    "explanation": f"出自{p['author']}的《{p['title']}》",
                    "difficulty": 1
                })
            else:
                p = random.choice(poems_db[:10])
                blank_count = random.randint(1, 2)
                content = p["content"]
                for _ in range(blank_count):
                    blank_pos = random.randint(2, len(content) - 2)
                    content = content[:blank_pos] + "___" + content[blank_pos+1:]
                
                questions.append({
                    "id": i+1, "type": "古诗填空", "topic": "古诗理解",
                    "question": f"《{p['title']}》({p['author']})\n{content}",
                    "answer": "略",  # 简化处理
                    "explanation": f"出自{p['author']}的《{p['title']}》",
                    "difficulty": 2
                })
    
    elif "初一" in grade or "初二" in grade:
        for i in range(count):
            p = random.choice(poems_db[5:12])
            questions.append({
                "id": i+1, "type": "古诗鉴赏", "topic": "诗词理解",
                "question": f"《{p['title']}》({p['author']}·{p['dynasty']})\n{p['content']}\n\n这首诗的主题是什么？",
                "answer": p["category"],
                "explanation": f"这首诗属于{p['category']}类诗歌，表达了诗人对{p['category']}的情感",
                "difficulty": 3
            })
    
    else:
        for i in range(count):
            p = random.choice(poems_db[10:])
            questions.append({
                "id": i+1, "type": "古诗鉴赏", "topic": "诗词鉴赏",
                "question": f"《{p['title']}》({p['author']}·{p['dynasty']})\n{p['content']}\n\n1.这首诗表达了什么情感？\n2.请赏析划线句",
                "answer": f"情感：{p['category']}\n赏析：情景交融，借景抒情",
                "explanation": f"诗人通过描写{p['category']}的景象，表达了内心情感",
                "difficulty": 4
            })
    
    return questions[:count]

def generate_english_questions(grade: str, count: int) -> List[Dict]:
    """生成英语题目"""
    questions = []
    
    vocab = ["apple", "book", "cat", "dog", "egg", "fish", "good", "happy", "I", "you"]
    sentences = [
        ("I ___ a student.", ["am", "is", "are"], "am"),
        ("She ___ apples every day.", ["eat", "eats", "eating"], "eats"),
        ("This is ___ book.", ["a", "an", "the"], "an"),
        ("There ___ two books on the desk.", ["is", "are", "am"], "are"),
        ("I ___ to school yesterday.", ["go", "went", "going"], "went"),
    ]
    
    for i in range(count):
        if i % 2 == 0:
            word = random.choice(vocab)
            questions.append({
                "id": i+1, "type": "单词拼写", "topic": "词汇",
                "question": f"请拼写这个单词：{word}",
                "answer": word,
                "explanation": f"单词：{word}",
                "difficulty": 1
            })
        else:
            sentence, options, ans = random.choice(sentences)
            questions.append({
                "id": i+1, "type": "选择题", "topic": "语法",
                "question": f"选择正确的答案：\n{sentence}",
                "options": options,
                "answer": ans,
                "explanation": f"根据语法规则，应选择 '{ans}'",
                "difficulty": 2
            })
    
    return questions[:count]

# ============ API 路由 ============

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

# ============ 核心API ============

@app.get("/api/children")
async def get_children():
    children = db.get_children()
    return {"children": children}

@app.post("/api/children")
async def add_child(request: Request):
    data = await request.json()
    name = data.get("name", "")
    grade = data.get("grade", "")
    avatar = data.get("avatar", "🧒")
    
    if not name or not grade:
        raise HTTPException(status_code=400, detail="姓名和年级不能为空")
    
    child = db.add_child(name, grade, avatar)
    return {"success": True, "child": child}

@app.put("/api/children/{child_id}")
async def update_child(child_id: int, request: Request):
    data = await request.json()
    success = db.update_child(child_id, **data)
    if success:
        child = db.get_child(child_id)
        return {"success": True, "child": child}
    raise HTTPException(status_code=404, detail="未找到该孩子")

@app.get("/api/models/list")
async def get_models():
    return {
        "models": [
            {"name": "qwen2.5:7b-instruct-q4_K_M", "desc": "通识问答"},
            {"name": "qwen-math:7b", "desc": "数学专项"},
            {"name": "qwen-coder:7b", "desc": "编程辅助"}
        ]
    }

@app.get("/api/diagnosis")
async def get_diagnosis(child_id: int = 1):
    child = db.get_child(child_id)
    if not child:
        return {"error": "未找到孩子"}
    
    progress = db.get_learning_progress(child_id)
    wrong = db.get_wrong_questions(child_id, reviewed=False)
    achievements = db.get_achievements(child_id)
    
    total = progress.get("total_questions", 0)
    correct = progress.get("correct_questions", 0)
    rate = f"{int(correct/total*100)}%" if total > 0 else "0%"
    
    return {
        "total_questions": total,
        "correct_rate": rate,
        "wrong_count": len(wrong),
        "study_time": progress.get("study_time", 0),
        "topics_mastered": len(progress.get("completed_topics", [])),
        "weak_points": progress.get("weak_points", [])[-5:],
        "strong_points": progress.get("strong_points", [])[-5:],
        "achievements": achievements,
        "points": child.get("points", 0),
        "level": child.get("level", 1),
        "streak": child.get("streak", 0)
    }

@app.get("/api/time")
async def get_time():
    now = datetime.now()
    lunar_key = now.strftime("%Y-%m-%d")
    lunar_date = await fetch_lunar_date(lunar_key)
    
    holidays_map = {
        "春节": (2, 17), "元宵节": (3, 3), "清明节": (4, 5),
        "劳动节": (5, 1), "端午节": (5, 31), "中秋节": (9, 25),
        "国庆节": (10, 1), "元旦": (1, 1)
    }
    
    holiday_today = ""
    for name, (m, d) in holidays_map.items():
        if now.month == m and now.day == d:
            holiday_today = name
            break
    
    return {
        "date": now.strftime("%Y年%m月%d日"),
        "time": now.strftime("%H:%M"),
        "weekday": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()],
        "lunar": lunar_date,
        "holiday": holiday_today,
        "season": "春季" if now.month in [3,4,5] else "夏季" if now.month in [6,7,8] else "秋季" if now.month in [9,10,11] else "冬季"
    }

@app.get("/api/time/countdown")
async def get_countdown(target: str):
    now = datetime.now()
    
    targets = {
        "春节": datetime(2027, 2, 6),
        "元宵": datetime(2027, 3, 3),
        "清明": datetime(2027, 4, 5),
        "劳动节": datetime(2027, 5, 1),
        "端午": datetime(2027, 5, 31),
        "中秋": datetime(2027, 9, 25),
        "国庆": datetime(2027, 10, 1),
        "元旦": datetime(2028, 1, 1),
        "儿童节": datetime(2027, 6, 1),
        "暑假": datetime(2027, 7, 1),
        "寒假": datetime(2027, 1, 15)
    }
    
    if target in targets:
        target_date = targets[target]
        delta = target_date - now
        
        if delta.days > 0:
            weeks = delta.days // 7
            return {"message": f"距离{target}还有 {delta.days} 天（约{weeks}周）🎉", "days": delta.days}
        elif delta.days == 0:
            return {"message": f"今天就是{target}！🎊", "days": 0}
        else:
            return {"message": f"{target}已经过去 {abs(delta.days)} 天了", "days": delta.days}
    
    return {"message": ""}

@app.get("/api/weather")
async def get_weather(city: str = "北京", tomorrow: bool = False):
    result, success = await fetch_weather(city, tomorrow)
    if success:
        return {"success": True, "data": result}
    return {"success": False, "error": "获取天气失败"}

@app.get("/api/topics")
async def get_topics():
    topics_list = db.get_topics()
    result = defaultdict(lambda: defaultdict(list))
    for t in topics_list:
        result[t["subject"]][t["grade"]].append(t["name"])
    return {"success": True, "topics": dict(result)}

@app.get("/api/topics/{subject}/{grade}")
async def get_grade_topics(subject: str, grade: str):
    topics_list = db.get_topics(subject, grade)
    return {"success": True, "topics": [t["name"] for t in topics_list]}

@app.get("/api/poems")
async def get_poems(category: str = None, difficulty: int = None):
    poems = db.get_poems(category, difficulty)
    return {"success": True, "poems": poems, "total": len(poems)}

@app.get("/api/knowledge")
async def get_knowledge(category: str = None):
    """获取知识百科"""
    articles = knowledge_articles
    if category:
        articles = [a for a in articles if category in a["tags"]]
    return {"success": True, "articles": articles, "total": len(articles)}

@app.post("/api/exam/generate")
async def generate_exam(request: Request):
    """生成练习题"""
    data = await request.json()
    grade = data.get("grade", "小学一年级")
    subject = data.get("subject", "数学")
    count = data.get("count", 10)
    topic = data.get("topic", None)
    
    if subject == "数学":
        questions = generate_math_questions(grade, count)
    elif subject == "语文":
        questions = generate_chinese_questions(grade, count)
    elif subject == "英语":
        questions = generate_english_questions(grade, count)
    else:
        questions = generate_math_questions(grade, count)
    
    if topic:
        questions = [q for q in questions if q.get("topic") == topic]
    
    return {"success": True, "questions": questions}

@app.post("/api/exam/submit")
async def submit_exam(request: Request):
    data = await request.json()
    child_id = data.get("child_id", 1)
    answers = data.get("answers", [])
    
    correct_count = 0
    total_questions = len(answers)
    
    for ans in answers:
        q_id = ans.get("question_id")
        user_ans = str(ans.get("answer", "")).strip()
        correct_ans = str(ans.get("correct_answer", "")).strip()
        
        if user_ans == correct_ans:
            correct_count += 1
        else:
            db.add_wrong_question(
                child_id=child_id,
                question=ans.get("question", ""),
                your_answer=user_ans,
                correct_answer=correct_ans,
                subject=ans.get("subject"),
                topic=ans.get("topic"),
                difficulty=ans.get("difficulty", 1)
            )
    
    progress = db.get_learning_progress(child_id)
    new_total = progress.get("total_questions", 0) + total_questions
    new_correct = progress.get("correct_questions", 0) + correct_count
    
    achievements = progress.get("achievements", [])
    if new_total >= 1 and "first_question" not in achievements:
        achievements.append("first_question")
        db.add_achievement(child_id, "first_question")
    
    db.update_learning_progress(
        child_id,
        total_questions=new_total,
        correct_questions=new_correct,
        achievements=achievements
    )
    
    child = db.get_child(child_id)
    if child:
        new_points = child.get("points", 0) + correct_count * 10
        new_level = new_points // 500 + 1
        db.update_child(child_id, points=new_points, level=new_level)
    
    return {
        "success": True,
        "total": total_questions,
        "correct": correct_count,
        "rate": f"{int(correct_count/total_questions*100)}%" if total_questions else "0%"
    }

@app.get("/api/wrong-questions")
async def get_wrong_questions(child_id: int = 1):
    questions = db.get_wrong_questions(child_id, reviewed=False)
    return {
        "success": True,
        "questions": questions,
        "total": len(questions)
    }

@app.post("/api/wrong-questions/review")
async def review_wrong_question(request: Request):
    data = await request.json()
    q_id = data.get("question_id")
    success = db.mark_wrong_question_reviewed(q_id)
    return {"success": success, "message": "复习完成！继续保持！"}

@app.get("/api/achievements")
async def get_achievements():
    """获取所有成就"""
    return {"success": True, "achievements": achievements}

@app.get("/api/achievements/{child_id}")
async def get_child_achievements(child_id: int = 1):
    earned_ids = db.get_achievements(child_id)
    earned = []
    for ach_id in earned_ids:
        if ach_id in achievements:
            earned.append({**achievements[ach_id], "id": ach_id})
    return {"success": True, "earned": earned, "total": len(achievements)}

@app.get("/api/learning-path")
async def get_learning_path(child_id: int = 1):
    child = db.get_child(child_id)
    if not child:
        return {"success": False, "error": "未找到孩子"}
    
    grade = child.get("grade", "小学一年级")
    topics_list = db.get_topics("数学", grade)
    
    path = {
        "current": {
            "level": child.get("level", 1),
            "points": child.get("points", 0),
            "next_level_points": (child.get("level", 1) + 1) * 500
        },
        "milestones": [
            {"name": "基础运算", "completed": child.get("level", 1) >= 1, "icon": "1️⃣"},
            {"name": "进阶计算", "completed": child.get("level", 1) >= 2, "icon": "2️⃣"},
            {"name": "应用题", "completed": child.get("level", 1) >= 4, "icon": "3️⃣"},
            {"name": "综合提升", "completed": child.get("level", 1) >= 6, "icon": "4️⃣"},
            {"name": "专家", "completed": child.get("level", 1) >= 10, "icon": "5️⃣"}
        ],
        "recommended_topics": [t["name"] for t in topics_list[:3]],
        "daily_tasks": [
            {"name": "完成10道练习题", "done": False, "points": 20},
            {"name": "复习2道错题", "done": False, "points": 10},
            {"name": "阅读1篇知识", "done": False, "points": 5}
        ]
    }
    
    return {"success": True, "path": path}

@app.get("/api/parent-report")
async def get_parent_report(child_id: int = 1):
    child = db.get_child(child_id)
    if not child:
        return {"success": False, "error": "未找到孩子"}
    
    progress = db.get_learning_progress(child_id)
    wrong = db.get_wrong_questions(child_id)
    records = db.get_study_records(child_id, days=7)
    
    total = progress.get("total_questions", 0)
    correct = progress.get("correct_questions", 0)
    
    weekly_progress = []
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    for i, day in enumerate(weekdays):
        record = records[i] if i < len(records) else None
        weekly_progress.append({
            "day": day,
            "questions": record.get("questions_count", random.randint(10, 30)) if record else random.randint(10, 30),
            "rate": f"{random.randint(70, 95)}%"
        })
    
    return {
        "success": True,
        "report": {
            "child_name": child.get("name", ""),
            "grade": child.get("grade", ""),
            "summary": {
                "total_questions": total,
                "correct_rate": f"{int(correct/total*100)}%" if total > 0 else "0%",
                "study_days": child.get("streak", 0),
                "total_points": child.get("points", 0),
                "level": child.get("level", 1)
            },
            "strengths": progress.get("strong_points", [])[-3:] or ["计算能力较好", "学习态度认真"],
            "weaknesses": progress.get("weak_points", [])[-3:] or ["应用题需要加强", "需要提高细心程度"],
            "weekly_progress": weekly_progress,
            "suggestions": [
                "建议每天固定时间学习，养成良好习惯",
                "错题本要及时复习，避免重复犯错",
                "适当增加阅读量，提高理解能力",
                "保持学习兴趣，不要给孩子太大压力"
            ],
            "next_week_goals": [
                "完成100道练习题",
                "正确率提升到90%",
                "坚持7天连续学习"
            ]
        }
    }

@app.get("/api/news")
async def get_news():
    """获取教育新闻"""
    return {
        "success": True,
        "news": [
            {"title": "教育部发布关于加强中小学人工智能教育的通知", "source": "教育部", "time": "2小时前"},
            {"title": "2027年高考时间确定，将于6月7-8日举行", "source": "教育部", "time": "5小时前"},
            {"title": "AI教育应用白皮书发布，揭示未来学习新趋势", "source": "教育周刊", "time": "1天前"},
            {"title": "多地学校开展AI辅助教学试点，效果显著", "source": "教育时报", "time": "2天前"}
        ]
    }

@app.post("/api/ollama/chat")
async def ollama_chat(request: Request):
    """AI聊天接口（模拟）"""
    data = await request.json()
    messages = data.get("messages", [])
    
    user_msg = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_msg = msg["content"]
            break
    
    async def generate():
        responses = [
            "你好！我是小熊老师🧸，很高兴为你服务！有什么学习问题尽管问我。",
            "这个知识点很重要！让我来给你详细讲解一下...",
            "学习需要循序渐进，我们一步一步来，加油！💪",
            "你问得很好！这个问题涉及到多个知识点，让我帮你梳理一下..."
        ]
        
        response = random.choice(responses)
        
        for char in response:
            yield f'{json.dumps({"message": {"content": char}}, ensure_ascii=False)}\n'
            await asyncio.sleep(0.03)
    
    return StreamingResponse(generate(), media_type="application/x-ndjson")

@app.post("/api/photo")
async def upload_photo(photo: UploadFile = File(...), child_id: int = 1):
    """照片识别"""
    content = await photo.read()
    return {
        "success": True,
        "result": "识别到的内容：\n1. 数学作业\n2. 计算题若干\n（实际需要OCR服务）"
    }

@app.post("/api/photo/grade")
async def grade_photo(request: Request):
    """批改照片"""
    data = await request.json()
    return {
        "success": True,
        "grade": {
            "correct": random.randint(7, 10),
            "total": 10,
            "wrong_questions": [
                {
                    "question": "25 + 17 = ?",
                    "your_answer": "41",
                    "correct_answer": "42"
                }
            ],
            "diagnosis": "计算能力不错，注意检查进位！"
        }
    }

@app.post("/api/plan/generate")
async def generate_plan(request: Request):
    """生成学习计划"""
    data = await request.json()
    child_id = data.get("child_id", 1)
    grade = data.get("grade", "小学一年级")
    subject = data.get("subject", "数学")
    
    child = next((c for c in children_data if c["id"] == child_id), children_data[0])
    
    return {
        "success": True,
        "plan": {
            "child_name": child["name"],
            "grade": grade,
            "goal": f"本周目标：提升{subject}能力，争取获得更多积分",
            "daily": [
                {"day": "周一", "tasks": ["复习上周内容", "完成10道练习"], "duration": "30分钟"},
                {"day": "周二", "tasks": ["学习新知识点", "做练习巩固"], "duration": "40分钟"},
                {"day": "周三", "tasks": ["错题复习", "阅读知识文章"], "duration": "35分钟"},
                {"day": "周四", "tasks": ["综合练习", "测试"], "duration": "45分钟"},
                {"day": "周五", "tasks": ["本周总结", "预习下周内容"], "duration": "30分钟"},
                {"day": "周六", "tasks": ["趣味学习", "游戏化练习"], "duration": "25分钟"},
                {"day": "周日", "tasks": ["休息放松", "亲子活动"], "duration": "0分钟"}
            ]
        }
    }

@app.get("/api/kb/list")
async def list_kb(child_id: int = 1):
    files = db.get_files(child_id)
    return {"success": True, "files": files}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), child_id: int = 1):
    upload_dir = DATA_DIR / "uploads"
    upload_dir.mkdir(exist_ok=True)
    
    file_location = upload_dir / file.filename
    content = await file.read()
    
    with open(file_location, "wb") as f:
        f.write(content)
    
    file_type = file.filename.split('.')[-1] if '.' in file.filename else 'unknown'
    
    db.add_file(
        child_id=child_id,
        filename=file.filename,
        file_path=str(file_location),
        file_size=len(content),
        file_type=file_type
    )
    
    return {"success": True, "message": "上传成功"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
