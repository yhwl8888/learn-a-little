#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一年级教材数据生成器
包含完整的一年级数学和语文教材内容
"""

from database import db
import random
from datetime import datetime

# ========== 一年级数学教材数据 ==========
GRADE1_MATH = {
    "chapters": [
        {
            "name": "准备课",
            "topics": ["数一数", "比多少"]
        },
        {
            "name": "位置",
            "topics": ["上、下、前、后", "左、右"]
        },
        {
            "name": "1-5的认识和加减法",
            "topics": ["1-5的认识", "比大小", "第几", "分与合", "加法", "减法", "0的认识"]
        },
        {
            "name": "认识图形（一）",
            "topics": ["认识立体图形", "拼搭图形"]
        },
        {
            "name": "6-10的认识和加减法",
            "topics": ["6和7的认识", "8和9的认识", "10的认识", "连加、连减", "加减混合"]
        },
        {
            "name": "11-20各数的认识",
            "topics": ["11-20各数的认识", "20以内的进位加法"]
        },
        {
            "name": "认识钟表",
            "topics": ["认识钟表"]
        },
        {
            "name": "20以内的退位减法",
            "topics": ["十几减9", "十几减8、7、6", "十几减5、4、3、2"]
        },
        {
            "name": "认识人民币",
            "topics": ["认识人民币", "简单的计算"]
        },
        {
            "name": "找规律",
            "topics": ["找规律"]
        }
    ]
}

# ========== 一年级语文教材数据 ==========
GRADE1_CHINESE = {
    "chapters": [
        {
            "name": "汉语拼音",
            "topics": ["a o e", "i u ü y w", "b p m f", "d t n l", 
                     "g k h", "j q x", "z c s", "zh ch sh r", 
                     "ai ei ui", "ao ou iu", "ie üe er", 
                     "an en in un ün", "ang eng ing ong"]
        },
        {
            "name": "识字（一）",
            "topics": ["天地人", "金木水火土", "口耳目", "日月水火", "对韵歌"]
        },
        {
            "name": "课文（一）",
            "topics": ["秋天", "小小的船", "江南", "四季"]
        },
        {
            "name": "识字（二）",
            "topics": ["画", "大小多少", "小书包", "日月明", "升国旗"]
        },
        {
            "name": "课文（二）",
            "topics": ["影子", "比尾巴", "青蛙写诗", "雨点儿", "明天要远足", "大还是小", "项链"]
        }
    ],
    "poems": [
        {
            "title": "江南",
            "author": "汉乐府",
            "dynasty": "汉",
            "content": "江南可采莲，莲叶何田田。鱼戏莲叶间。鱼戏莲叶东，鱼戏莲叶西，鱼戏莲叶南，鱼戏莲叶北。",
            "category": "古诗",
            "difficulty": 2
        },
        {
            "title": "画",
            "author": "佚名",
            "dynasty": "唐",
            "content": "远看山有色，近听水无声。春去花还在，人来鸟不惊。",
            "category": "古诗",
            "difficulty": 2
        },
        {
            "title": "悯农",
            "author": "李绅",
            "dynasty": "唐",
            "content": "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。",
            "category": "古诗",
            "difficulty": 2
        },
        {
            "title": "静夜思",
            "author": "李白",
            "dynasty": "唐",
            "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
            "category": "古诗",
            "difficulty": 2
        }
    ]
}

# ========== 数学题生成器 ==========
def generate_math_questions():
    questions = []
    
    # 1-5的加法
    for i in range(1, 6):
        for j in range(1, 6):
            questions.append({
                "subject": "数学",
                "grade": "小学一年级",
                "topic": "1-5的认识和加减法",
                "question_type": "口算题",
                "question_text": f"{i} + {j} = ?",
                "answer": str(i + j),
                "explanation": f"{i} 加上 {j} 等于 {i + j}",
                "difficulty": 1
            })
    
    # 1-5的减法
    for i in range(2, 6):
        for j in range(1, i+1):
            questions.append({
                "subject": "数学",
                "grade": "小学一年级",
                "topic": "1-5的认识和加减法",
                "question_type": "口算题",
                "question_text": f"{i} - {j} = ?",
                "answer": str(i - j),
                "explanation": f"{i} 减去 {j} 等于 {i - j}",
                "difficulty": 1
            })
    
    # 6-10的加法
    for i in range(1, 11):
        for j in range(1, 11):
            if i + j <= 20:
                questions.append({
                    "subject": "数学",
                    "grade": "小学一年级",
                    "topic": "6-10的认识和加减法",
                    "question_type": "口算题",
                    "question_text": f"{i} + {j} = ?",
                    "answer": str(i + j),
                    "explanation": f"{i} 加上 {j} 等于 {i + j}",
                    "difficulty": 2
                })
    
    # 简单应用题
    scenarios = [
        ("有3个苹果，又买了2个，一共有几个？", 5),
        ("有10块糖，吃了3块，还剩几块？", 7),
        ("小明有5个玩具，小红有4个，一共有几个？", 9),
        ("妈妈买了8个梨，吃了5个，还剩几个？", 3),
        ("树上有7只鸟，又飞来3只，现在有几只？", 10),
        ("书架上有6本书，拿走了2本，还剩几本？", 4)
    ]
    
    for q_text, ans in scenarios:
        questions.append({
            "subject": "数学",
            "grade": "小学一年级",
            "topic": "6-10的认识和加减法",
            "question_type": "应用题",
            "question_text": q_text,
            "answer": str(ans),
            "explanation": f"根据题意计算，答案是 {ans}",
            "difficulty": 2
        })
    
    # 比大小
    numbers = [(1,2), (3,1), (4,4), (2,5), (5,3)]
    for a, b in numbers:
        correct = "=" if a == b else ">" if a > b else "<"
        questions.append({
            "subject": "数学",
            "grade": "小学一年级",
            "topic": "比大小",
            "question_type": "填空题",
            "question_text": f"{a} ○ {b} （填 >、< 或 =）",
            "answer": correct,
            "explanation": f"{a} {correct} {b}",
            "difficulty": 1
        })
    
    return questions

# ========== 语文题生成器 ==========
def generate_chinese_questions():
    questions = []
    
    # 生字拼音
    chars = [
        ("天", "tiān"), ("地", "dì"), ("人", "rén"),
        ("你", "nǐ"), ("我", "wǒ"), ("他", "tā"),
        ("一", "yī"), ("二", "èr"), ("三", "sān"),
        ("四", "sì"), ("五", "wǔ"), ("上", "shàng"),
        ("下", "xià"), ("日", "rì"), ("月", "yuè")
    ]
    
    for char, pinyin in chars:
        questions.append({
            "subject": "语文",
            "grade": "小学一年级",
            "topic": "汉语拼音",
            "question_type": "拼音题",
            "question_text": f"请写出\"{char}\"的拼音",
            "answer": pinyin,
            "explanation": f"\"{char}\"的拼音是 {pinyin}",
            "difficulty": 1
        })
    
    # 反义词
    antonyms = [
        ("大", "小"), ("多", "少"), ("上", "下"),
        ("左", "右"), ("前", "后"), ("东", "西"),
        ("南", "北"), ("天", "地"), ("有", "无")
    ]
    
    for word, antonym in antonyms:
        questions.append({
            "subject": "语文",
            "grade": "小学一年级",
            "topic": "识字",
            "question_type": "填空题",
            "question_text": f"\"{word}\"的反义词是什么？",
            "answer": antonym,
            "explanation": f"\"{word}\"的反义词是\"{antonym}\"",
            "difficulty": 1
        })
    
    # 古诗填空
    poems = [
        ("江南可采莲，莲叶何____。", "田田"),
        ("鱼戏莲叶____。", "间"),
        ("远看山有____，近听水无声。", "色"),
        ("春去花还在，____来鸟不惊。", "人"),
        ("草芽尖尖，他对小鸟说：'我是____。'", "春天")
    ]
    
    for q_text, ans in poems:
        questions.append({
            "subject": "语文",
            "grade": "小学一年级",
            "topic": "古诗",
            "question_type": "填空题",
            "question_text": q_text,
            "answer": ans,
            "explanation": "根据古诗内容填空",
            "difficulty": 2
        })
    
    # 组词
    words = [
        ("天", ["天空", "天地", "白天"]),
        ("地", ["土地", "大地", "地方"]),
        ("人", ["人们", "大人", "人口"]),
        ("山", ["大山", "山水", "上山"]),
        ("水", ["水果", "水牛", "河水"])
    ]
    
    for char, groups in words:
        questions.append({
            "subject": "语文",
            "grade": "小学一年级",
            "topic": "识字",
            "question_type": "组词题",
            "question_text": f"用\"{char}\"组三个词",
            "answer": "、".join(groups),
            "explanation": f"可以组成：{'、'.join(groups)}",
            "difficulty": 2
        })
    
    return questions

# ========== 数据导入函数 ==========
def import_grade1_data():
    print("="*60)
    print("开始导入一年级教材数据")
    print("="*60)
    
    # 先清除可能存在的旧数据
    conn = db._get_connection()
    cursor = conn.cursor()
    
    # 导入数学知识点
    print("\n【1】导入一年级数学知识点...")
    math_topic_data = []
    for chapter in GRADE1_MATH["chapters"]:
        chapter_name = chapter["name"]
        for topic in chapter["topics"]:
            math_topic_data.append((
                "数学", 
                "小学一年级", 
                topic, 
                f"{chapter_name} - {topic}"
            ))
    
    cursor.executemany(
        "INSERT OR IGNORE INTO topics (subject, grade, name, description) VALUES (?, ?, ?, ?)",
        math_topic_data
    )
    conn.commit()
    print(f"  ✓ 导入数学知识点: {len(math_topic_data)} 个")
    
    # 导入语文知识点
    print("\n【2】导入一年级语文知识点...")
    chinese_topic_data = []
    for chapter in GRADE1_CHINESE["chapters"]:
        chapter_name = chapter["name"]
        for topic in chapter["topics"]:
            chinese_topic_data.append((
                "语文", 
                "小学一年级", 
                topic, 
                f"{chapter_name} - {topic}"
            ))
    
    cursor.executemany(
        "INSERT OR IGNORE INTO topics (subject, grade, name, description) VALUES (?, ?, ?, ?)",
        chinese_topic_data
    )
    conn.commit()
    print(f"  ✓ 导入语文知识点: {len(chinese_topic_data)} 个")
    
    # 导入古诗词
    print("\n【3】导入一年级古诗词...")
    poem_data = []
    for poem in GRADE1_CHINESE["poems"]:
        poem_data.append((
            poem["title"],
            poem["author"],
            poem["dynasty"],
            poem["content"],
            poem["category"],
            poem["difficulty"]
        ))
    
    cursor.executemany(
        "INSERT OR IGNORE INTO poems (title, author, dynasty, content, category, difficulty) VALUES (?, ?, ?, ?, ?, ?)",
        poem_data
    )
    conn.commit()
    print(f"  ✓ 导入古诗词: {len(poem_data)} 首")
    
    # 导入数学题目
    print("\n【4】生成并导入一年级数学题目...")
    math_questions = generate_math_questions()
    for q in math_questions:
        db.add_question(
            subject=q["subject"],
            grade=q["grade"],
            question_type=q["question_type"],
            question_text=q["question_text"],
            answer=q["answer"],
            topic=q["topic"],
            explanation=q["explanation"],
            difficulty=q["difficulty"],
            options=q.get("options")
        )
    print(f"  ✓ 导入数学题目: {len(math_questions)} 道")
    
    # 导入语文题目
    print("\n【5】生成并导入一年级语文题目...")
    chinese_questions = generate_chinese_questions()
    for q in chinese_questions:
        db.add_question(
            subject=q["subject"],
            grade=q["grade"],
            question_type=q["question_type"],
            question_text=q["question_text"],
            answer=q["answer"],
            topic=q["topic"],
            explanation=q["explanation"],
            difficulty=q["difficulty"],
            options=q.get("options")
        )
    print(f"  ✓ 导入语文题目: {len(chinese_questions)} 道")
    
    print("\n" + "="*60)
    print("一年级教材数据导入完成！")
    print("="*60)
    total = len(math_topic_data) + len(chinese_topic_data) + len(poem_data) + len(math_questions) + len(chinese_questions)
    print(f"\n统计:")
    print(f"  数学知识点: {len(math_topic_data)}")
    print(f"  语文知识点: {len(chinese_topic_data)}")
    print(f"  古诗词: {len(poem_data)}")
    print(f"  数学题目: {len(math_questions)}")
    print(f"  语文题目: {len(chinese_questions)}")
    print(f"  总计: {total} 条")

# ========== 查询和展示函数 ==========
def show_grade1_summary():
    print("\n" + "="*60)
    print("一年级教材数据概览")
    print("="*60)
    
    # 查询知识点
    math_topics = db.get_topics(subject="数学", grade="小学一年级")
    chinese_topics = db.get_topics(subject="语文", grade="小学一年级")
    print(f"\n数学知识点: {len(math_topics)} 个")
    print(f"语文知识点: {len(chinese_topics)} 个")
    
    # 查询题目
    math_questions = db.get_questions(subject="数学", grade="小学一年级", limit=5)
    chinese_questions = db.get_questions(subject="语文", grade="小学一年级", limit=5)
    print(f"\n数学题目示例:")
    for i, q in enumerate(math_questions[:3], 1):
        print(f"  {i}. {q['question_text']}")
    
    print(f"\n语文题目示例:")
    for i, q in enumerate(chinese_questions[:3], 1):
        print(f"  {i}. {q['question_text']}")
    
    # 查询诗词
    poems = db.get_poems()
    print(f"\n古诗词: {len(poems)} 首")
    for p in poems[:3]:
        print(f"  《{p['title']}》 - {p['author']}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    # 导入数据
    import_grade1_data()
    
    # 显示摘要
    show_grade1_summary()
