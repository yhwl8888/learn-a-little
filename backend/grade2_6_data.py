#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二到六年级教材数据生成器
包含完整的数学和语文知识点及题目生成
"""

import random
from database import db

# ========== 二到六年级数学知识点 ==========
GRADE_MATH = {
    "小学二年级": {
        "chapters": [
            {"name": "长度单位", "topics": ["认识厘米和米", "认识线段", "简单的测量"]},
            {"name": "100以内的加法和减法（二）", "topics": ["两位数加两位数", "两位数减两位数", "连加连减", "加减混合", "解决问题"]},
            {"name": "角的初步认识", "topics": ["认识角", "认识直角", "认识锐角和钝角"]},
            {"name": "表内乘法（一）", "topics": ["乘法的初步认识", "2-6的乘法口诀", "乘加乘减"]},
            {"name": "观察物体（一）", "topics": ["观察立体图形", "从不同位置观察"]},
            {"name": "表内乘法（二）", "topics": ["7的乘法口诀", "8的乘法口诀", "9的乘法口诀"]},
            {"name": "认识时间", "topics": ["认识分", "认识几时几分", "解决问题"]},
            {"name": "数学广角", "topics": ["搭配问题"]}
        ]
    },
    "小学三年级": {
        "chapters": [
            {"name": "时、分、秒", "topics": ["认识秒", "时间的计算", "解决问题"]},
            {"name": "万以内的加法和减法（一）", "topics": ["两位数加两位数口算", "两位数减两位数口算", "笔算", "验算"]},
            {"name": "测量", "topics": ["毫米、分米的认识", "千米的认识", "吨的认识"]},
            {"name": "倍的认识", "topics": ["倍的意义", "求一个数是另一个数的几倍", "求一个数的几倍是多少"]},
            {"name": "多位数乘一位数", "topics": ["口算乘法", "笔算乘法", "有关0的乘法", "解决问题"]},
            {"name": "长方形和正方形", "topics": ["四边形的认识", "长方形和正方形的特征", "周长的认识", "长方形和正方形的周长"]},
            {"name": "分数的初步认识", "topics": ["几分之一", "几分之几", "分数的简单计算"]},
            {"name": "数学广角", "topics": ["集合"]}
        ]
    },
    "小学四年级": {
        "chapters": [
            {"name": "大数的认识", "topics": ["亿以内数的认识", "数的产生", "十进制计数法", "亿以上数的认识", "计算工具的认识"]},
            {"name": "公顷和平方千米", "topics": ["公顷的认识", "平方千米的认识"]},
            {"name": "角的度量", "topics": ["线段、直线、射线", "角的概念", "角的度量", "角的分类", "画角"]},
            {"name": "三位数乘两位数", "topics": ["口算乘法", "笔算乘法", "速度的认识", "解决问题"]},
            {"name": "平行四边形和梯形", "topics": ["平行与垂直", "平行四边形", "梯形"]},
            {"name": "除数是两位数的除法", "topics": ["口算除法", "笔算除法", "商的变化规律"]},
            {"name": "条形统计图", "topics": ["认识条形统计图", "绘制条形统计图"]},
            {"name": "数学广角", "topics": ["优化"]}
        ]
    },
    "小学五年级": {
        "chapters": [
            {"name": "小数乘法", "topics": ["小数乘整数", "小数乘小数", "积的近似数", "整数乘法运算定律推广到小数"]},
            {"name": "位置", "topics": ["用数对表示位置", "在方格纸上用数对确定位置"]},
            {"name": "小数除法", "topics": ["除数是整数的小数除法", "一个数除以小数", "商的近似数", "循环小数", "用计算器探索规律"]},
            {"name": "可能性", "topics": ["可能性", "掷一掷"]},
            {"name": "简易方程", "topics": ["用字母表示数", "方程的意义", "解方程", "实际问题与方程"]},
            {"name": "多边形的面积", "topics": ["平行四边形的面积", "三角形的面积", "梯形的面积", "组合图形的面积"]},
            {"name": "数学广角", "topics": ["植树问题"]}
        ]
    },
    "小学六年级": {
        "chapters": [
            {"name": "分数乘法", "topics": ["分数乘整数", "分数乘分数", "小数乘分数", "分数混合运算", "解决问题"]},
            {"name": "位置与方向（二）", "topics": ["用方向和距离确定位置", "描述路线图"]},
            {"name": "分数除法", "topics": ["倒数的认识", "分数除法", "解决问题"]},
            {"name": "比", "topics": ["比的意义", "基本性质", "比的应用"]},
            {"name": "圆", "topics": ["圆的认识", "圆的周长", "圆的面积", "扇形"]},
            {"name": "百分数（一）", "topics": ["百分数的意义", "小数、分数化成百分数", "百分数化成小数、分数", "解决问题"]},
            {"name": "扇形统计图", "topics": ["认识扇形统计图", "选择合适的统计图"]},
            {"name": "数学广角", "topics": ["数与形"]}
        ]
    }
}

# ========== 二到六年级语文知识点 ==========
GRADE_CHINESE = {
    "小学二年级": {
        "chapters": [
            {"name": "识字", "topics": ["场景歌", "树之歌", "拍手歌", "田家四季歌"]},
            {"name": "课文", "topics": ["小蝌蚪找妈妈", "我是什么", "植物妈妈有办法", "曹冲称象", "玲玲的画", "一封信", "妈妈睡了", "古诗二首", "黄山奇石", "日月潭", "葡萄沟", "坐井观天", "寒号鸟", "我要的是葫芦"]},
            {"name": "语文园地", "topics": ["口语交际", "写话", "日积月累"]}
        ]
    },
    "小学三年级": {
        "chapters": [
            {"name": "课文", "topics": ["大青树下的小学", "花的学校", "不懂就要问", "古诗三首", "秋天的雨", "听听，秋的声音", "卖火柴的小女孩", "那一定会很好", "在牛肚子里旅行", "一块奶酪", "总也倒不了的老屋", "胡萝卜先生的长胡子", "小狗学叫"]},
            {"name": "写作", "topics": ["写日记", "写日记", "我来编童话", "续写故事", "我们眼中的缤纷世界", "这儿真美", "那次玩得真高兴"]},
            {"name": "古诗", "topics": ["山行", "赠刘景文", "夜书所见", "望天门山", "饮湖上初晴后雨", "望洞庭"]}
        ]
    },
    "小学四年级": {
        "chapters": [
            {"name": "课文", "topics": ["观潮", "走月亮", "现代诗二首", "繁星", "一个豆荚里的五粒豆", "蝙蝠和雷达", "呼风唤雨的世纪", "蝴蝶的家", "古诗三首", "爬山虎的脚", "蟋蟀的住宅", "盘古开天地", "精卫填海", "普罗米修斯", "女娲补天", "麻雀", "爬天都峰"]},
            {"name": "写作", "topics": ["写日记", "写观察日记", "写童话", "写绿豆", "写写小动物", "写导游词", "写信", "写我的心儿怦怦跳"]},
            {"name": "古诗", "topics": ["暮江吟", "题西林壁", "雪梅", "出塞", "凉州词", "夏日绝句", "别董大"]}
        ]
    },
    "小学五年级": {
        "chapters": [
            {"name": "课文", "topics": ["白鹭", "落花生", "桂花雨", "珍珠鸟", "搭石", "将相和", "什么比猎豹的速度更快", "冀中的地道战", "猎人海力布", "牛郎织女", "父爱之舟", "精彩极了和糟糕透了", "圆明园的毁灭", "七律·长征", "狼牙山五壮士", "开国大典", "灯光", "松鼠", "慈母情深", "父爱之舟"]},
            {"name": "古诗", "topics": ["山居秋暝", "枫桥夜泊", "长相思", "渔歌子", "示儿", "题临安邸", "已亥杂诗", "少年中国说", "四季之美", "鸟的天堂", "月迹"]},
            {"name": "文言文", "topics": ["少年中国说", "古人谈读书", "忆读书"]}
        ]
    },
    "小学六年级": {
        "chapters": [
            {"name": "课文", "topics": ["草原", "丁香结", "古诗词三首", "花之歌", "七律·长征", "狼牙山五壮士", "开国大典", "灯光", "我的战友邱少云", "竹节人", "宇宙生命之谜", "故宫博物院", "桥", "穷人", "在柏林", "夏天里的成长", "盼", "古诗三首", "少年闰土", "好的故事", "我的伯父鲁迅先生", "有的人", "伯牙鼓琴", "书戴嵩画牛"]},
            {"name": "古诗词", "topics": ["宿建德江", "六月二十七日望湖楼醉书", "西江月·夜行黄沙道中", "过故人庄", "鲁山山行", "野望", "渡荆门送别", "钱塘湖春行", "饮酒", "春望", "雁门太守行", "赤壁", "渔家傲", "江城子·密州出猎", "破阵子", "满江红", "十五夜望月", "已亥杂诗"]},
            {"name": "文言文", "topics": ["伯牙鼓琴", "书戴嵩画牛", "学弈", "两小儿辩日"]}
        ]
    }
}

# ========== 数学题目生成器 ==========
def generate_math_question(grade, topic):
    """根据年级和知识点生成数学题目"""
    
    questions = []
    
    if "加法" in topic or "减法" in topic:
        if "两位数" in topic:
            for _ in range(10):
                a = random.randint(10, 99)
                b = random.randint(10, 99)
                if "加" in topic:
                    questions.append({
                        "subject": "数学",
                        "grade": grade,
                        "topic": topic,
                        "question_type": "计算题",
                        "question_text": f"{a} + {b} = ?",
                        "answer": str(a + b),
                        "explanation": f"{a} + {b} = {a + b}",
                        "difficulty": 2
                    })
                elif "减" in topic:
                    a, b = max(a, b), min(a, b)
                    questions.append({
                        "subject": "数学",
                        "grade": grade,
                        "topic": topic,
                        "question_type": "计算题",
                        "question_text": f"{a} - {b} = ?",
                        "answer": str(a - b),
                        "explanation": f"{a} - {b} = {a - b}",
                        "difficulty": 2
                    })
        
        elif "万以内" in topic:
            for _ in range(8):
                a = random.randint(1000, 9999)
                b = random.randint(100, 999)
                if "加" in topic:
                    questions.append({
                        "subject": "数学",
                        "grade": grade,
                        "topic": topic,
                        "question_type": "计算题",
                        "question_text": f"{a} + {b} = ?",
                        "answer": str(a + b),
                        "explanation": f"{a} + {b} = {a + b}",
                        "difficulty": 3
                    })
                elif "减" in topic:
                    a = random.randint(2000, 9999)
                    b = random.randint(1000, a)
                    questions.append({
                        "subject": "数学",
                        "grade": grade,
                        "topic": topic,
                        "question_type": "计算题",
                        "question_text": f"{a} - {b} = ?",
                        "answer": str(a - b),
                        "explanation": f"{a} - {b} = {a - b}",
                        "difficulty": 3
                    })
    
    elif "乘法" in topic:
        if "一位数" in topic or "多位数乘一位数" in topic:
            for _ in range(12):
                a = random.randint(100, 999)
                b = random.randint(2, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a} × {b} = ?",
                    "answer": str(a * b),
                    "explanation": f"{a} × {b} = {a * b}",
                    "difficulty": 3
                })
        elif "两位数乘两位数" in topic or "三位数乘两位数" in topic:
            for _ in range(10):
                if "两位" in topic:
                    a = random.randint(10, 99)
                    b = random.randint(10, 99)
                else:
                    a = random.randint(100, 999)
                    b = random.randint(10, 99)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a} × {b} = ?",
                    "answer": str(a * b),
                    "explanation": f"{a} × {b} = {a * b}",
                    "difficulty": 4
                })
        else:
            for _ in range(8):
                a = random.randint(2, 9)
                b = random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "口算题",
                    "question_text": f"{a} × {b} = ?",
                    "answer": str(a * b),
                    "explanation": f"{a} × {b} = {a * b}，使用乘法口诀",
                    "difficulty": 2
                })
    
    elif "除法" in topic:
        if "两位数除以一位数" in topic or "除数是整数" in topic:
            for _ in range(12):
                b = random.randint(2, 9)
                a = b * random.randint(10, 99)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a} ÷ {b} = ?",
                    "answer": str(a // b),
                    "explanation": f"{a} ÷ {b} = {a // b}",
                    "difficulty": 3
                })
        elif "除数是两位数" in topic:
            for _ in range(10):
                b = random.randint(10, 99)
                a = b * random.randint(10, 50)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a} ÷ {b} = ?",
                    "answer": str(a // b),
                    "explanation": f"{a} ÷ {b} = {a // b}",
                    "difficulty": 4
                })
        else:
            for _ in range(8):
                b = random.randint(2, 9)
                a = b * random.randint(2, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "口算题",
                    "question_text": f"{a} ÷ {b} = ?",
                    "answer": str(a // b),
                    "explanation": f"{a} ÷ {b} = {a // b}",
                    "difficulty": 2
                })
    
    elif "分数" in topic:
        if "乘法" in topic:
            for _ in range(10):
                a, b = random.randint(1, 9), random.randint(1, 9)
                c = random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a}/{b} × {c} = ?",
                    "answer": f"{a*c}//{b}" if b != 1 else str(a*c),
                    "explanation": f"{a}/{b} × {c} = {a*c}/{b}",
                    "difficulty": 3
                })
        elif "除法" in topic:
            for _ in range(10):
                a, b = random.randint(1, 9), random.randint(1, 9)
                c = random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a}/{b} ÷ {c} = ?",
                    "answer": f"{a}//{b*c}" if a == 1 else f"{a}//{b*c}",
                    "explanation": f"{a}/{b} ÷ {c} = {a}/{b*c}",
                    "difficulty": 3
                })
        else:
            for _ in range(8):
                a, b = random.randint(1, 9), random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "填空题",
                    "question_text": f"{min(a,b)}/{max(a,b)} 比大小，{a}/{b}（填 >、< 或 =）",
                    "answer": ">" if a > b else "<" if a < b else "=",
                    "explanation": f"{a}/{b}",
                    "difficulty": 2
                })
    
    elif "小数" in topic:
        if "乘法" in topic:
            for _ in range(10):
                a = random.randint(1, 99) / 10
                b = random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a} × {b} = ?（保留两位小数）",
                    "answer": f"{a * b:.2f}",
                    "explanation": f"{a} × {b} = {a * b:.2f}",
                    "difficulty": 3
                })
        elif "除法" in topic:
            for _ in range(10):
                a = random.randint(1, 99) / 10
                b = random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a} ÷ {b} = ?（保留两位小数）",
                    "answer": f"{a / b:.2f}",
                    "explanation": f"{a} ÷ {b} = {a / b:.2f}",
                    "difficulty": 3
                })
    
    elif "面积" in topic or "周长" in topic:
        for _ in range(6):
            length = random.randint(2, 20)
            width = random.randint(2, 20)
            if "周长" in topic:
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "应用题",
                    "question_text": f"一个长方形，长{length}厘米，宽{width}厘米，周长是多少？",
                    "answer": f"{(length + width) * 2}",
                    "explanation": f"周长 = (长 + 宽) × 2 = ({length} + {width}) × 2 = {(length + width) * 2}厘米",
                    "difficulty": 2
                })
            else:
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "应用题",
                    "question_text": f"一个长方形，长{length}厘米，宽{width}厘米，面积是多少？",
                    "answer": f"{length * width}",
                    "explanation": f"面积 = 长 × 宽 = {length} × {width} = {length * width}平方厘米",
                    "difficulty": 2
                })
    
    elif "速度" in topic or "路程" in topic:
        for _ in range(5):
            speed = random.randint(30, 120)
            time = random.randint(1, 5)
            questions.append({
                "subject": "数学",
                "grade": grade,
                "topic": topic,
                "question_type": "应用题",
                "question_text": f"一辆汽车的速度是{speed}千米/时，行驶{time}小时，路程是多少？",
                "answer": f"{speed * time}",
                "explanation": f"路程 = 速度 × 时间 = {speed} × {time} = {speed * time}千米",
                "difficulty": 3
            })
    
    return questions

# ========== 语文题目生成器 ==========
def generate_chinese_question(grade, topic):
    """根据年级和知识点生成语文题目"""
    
    questions = []
    
    # 古诗相关
    poems_grade2 = [
        {"title": "登鹳雀楼", "author": "王之涣", "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。"},
        {"title": "望庐山瀑布", "author": "李白", "content": "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。"},
    ]
    
    poems_grade3 = [
        {"title": "山行", "author": "杜牧", "content": "远上寒山石径斜，白云生处有人家。停车坐爱枫林晚，霜叶红于二月花。"},
        {"title": "赠刘景文", "author": "苏轼", "content": "荷尽已无擎雨盖，菊残犹有傲霜枝。一年好景君须记，正是橙黄橘绿时。"},
        {"title": "夜书所见", "author": "叶绍翁", "content": "萧萧梧叶送寒声，江上秋风动客情。知有儿童挑促织，夜深篱落一灯明。"},
    ]
    
    poems_grade4 = [
        {"title": "暮江吟", "author": "白居易", "content": "一道残阳铺水中，半江瑟瑟半江红。可怜九月初三夜，露似真珠月似弓。"},
        {"title": "题西林壁", "author": "苏轼", "content": "横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。"},
        {"title": "雪梅", "author": "卢梅坡", "content": "梅雪争春未肯降，骚人搁笔费评章。梅须逊雪三分白，雪却输梅一段香。"},
    ]
    
    poems_grade5 = [
        {"title": "示儿", "author": "陆游", "content": "死去元知万事空，但悲不见九州同。王师北定中原日，家祭无忘告乃翁。"},
        {"title": "题临安邸", "author": "林升", "content": "山外青山楼外楼，西湖歌舞几时休？暖风熏得游人醉，直把杭州作汴州。"},
        {"title": "已亥杂诗", "author": "龚自珍", "content": "九州生气恃风雷，万马齐喑究可哀。我劝天公重抖擞，不拘一格降人才。"},
    ]
    
    poems_grade6 = [
        {"title": "宿建德江", "author": "孟浩然", "content": "移舟泊烟渚，日暮客愁新。野旷天低树，江清月近人。"},
        {"title": "六月二十七日望湖楼醉书", "author": "苏轼", "content": "黑云翻墨未遮山，白雨跳珠乱入船。卷地风来忽吹散，望湖楼下水如天。"},
        {"title": "西江月·夜行黄沙道中", "author": "辛弃疾", "content": "明月别枝惊鹊，清风半夜鸣蝉。稻花香里说丰年，听取蛙声一片。"},
    ]
    
    all_poems = {
        "小学二年级": poems_grade2,
        "小学三年级": poems_grade3,
        "小学四年级": poems_grade4,
        "小学五年级": poems_grade5,
        "小学六年级": poems_grade6
    }
    
    # 古诗题目
    if "古诗" in topic or "古诗词" in topic or "古文" in topic or "诗" in topic:
        poems = all_poems.get(grade, poems_grade3)
        for poem in poems:
            # 诗句填空
            lines = poem["content"].split("，")
            for line in lines[:2]:
                words = list(line)
                if len(words) >= 4:
                    idx = random.randint(2, len(words) - 2)
                    question = line[:idx] + "____" + line[idx+1:]
                    questions.append({
                        "subject": "语文",
                        "grade": grade,
                        "topic": topic,
                        "question_type": "古诗填空",
                        "question_text": f"《{poem['title']》({poem['author']})\n{question}",
                        "answer": words[idx],
                        "explanation": f"出自{poem['author']}的《{poem['title']}》",
                        "difficulty": 2
                    })
            
            # 诗意理解
            questions.append({
                "subject": "语文",
                "grade": grade,
                "topic": topic,
                "question_type": "古诗理解",
                "question_text": f"《{poem['title']》这首诗表达了什么情感？",
                "answer": "借景抒情",
                "explanation": f"《{poem['title']}》通过描写景物来表达诗人情感",
                "difficulty": 3
            })
    
    # 文言文相关
    if "文言文" in topic or "学弈" in topic or "两小儿辩日" in topic:
        questions.append({
            "subject": "语文",
            "grade": grade,
            "topic": topic,
            "question_type": "文言文理解",
            "question_text": f"解释"学弈"中"之"字的用法",
            "answer": "助词，的",
            "explanation": "学习下棋时发生的事情",
            "difficulty": 3
        })
    
    # 课文理解
    if "课文" in topic:
        # 近义词反义词
        antonyms_pairs = [
            ("高", "低"), ("远", "近"), ("快", "慢"), ("粗", "细"),
            ("容易", "困难"), ("打开", "关闭"), ("上升", "下降"), ("胜利", "失败")
        ]
        for _ in range(3):
            word, antonym = random.choice(antonyms_pairs)
            questions.append({
                "subject": "语文",
                "grade": grade,
                "topic": topic,
                "question_type": "词语理解",
                "question_text": f"写出"{word}"的反义词",
                "answer": antonym,
                "explanation": f"{word}的反义词是{antonym}",
                "difficulty": 2
            })
        
        # 修辞手法
        questions.append({
            "subject": "语文",
            "grade": grade,
            "topic": topic,
            "question_type": "修辞手法",
            "question_text": "下列句子使用了什么修辞手法："荷叶挨挨挤挤的，像一个个碧绿的大圆盘。"",
            "answer": "比喻",
            "explanation": "把荷叶比作大圆盘，是比喻中的明喻",
            "difficulty": 2
        })
    
    # 写作相关
    if "写作" in topic or "写话" in topic:
        questions.append({
            "subject": "语文",
            "grade": grade,
            "topic": topic,
            "question_type": "写作题",
            "question_text": f"根据题目"{topic.replace('写作', '').replace('写话', '练习')}"写一段话（不少于100字）",
            "answer": "开放题，言之有理即可",
            "explanation": "考查写作能力，注意条理清晰",
            "difficulty": 3
        })
    
    return questions

# ========== 数据导入函数 ==========
def import_all_data():
    print("="*60)
    print("开始导入二到六年级教材数据")
    print("="*60)
    
    conn = db._get_connection()
    cursor = conn.cursor()
    
    total_topics = 0
    total_questions = 0
    
    # 导入数学知识点和题目
    print("\n【1】导入二到六年级数学知识点...")
    math_topic_data = []
    for grade, data in GRADE_MATH.items():
        for chapter in data["chapters"]:
            chapter_name = chapter["name"]
            for topic in chapter["topics"]:
                math_topic_data.append((
                    "数学",
                    grade,
                    topic,
                    f"{chapter_name} - {topic}"
                ))
                total_topics += 1
                
                # 生成该知识点的题目
                questions = generate_math_question(grade, topic)
                for q in questions:
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
                    total_questions += 1
    
    cursor.executemany(
        "INSERT OR IGNORE INTO topics (subject, grade, name, description) VALUES (?, ?, ?, ?)",
        math_topic_data
    )
    conn.commit()
    print(f"  ✓ 导入数学知识点: {len(math_topic_data)} 个")
    print(f"  ✓ 生成数学题目: {total_questions} 道")
    
    # 导入语文知识点和题目
    print("\n【2】导入二到六年级语文知识点...")
    chinese_topic_data = []
    chinese_questions_count = 0
    for grade, data in GRADE_CHINESE.items():
        for chapter in data["chapters"]:
            chapter_name = chapter["name"]
            for topic in chapter["topics"]:
                chinese_topic_data.append((
                    "语文",
                    grade,
                    topic,
                    f"{chapter_name} - {topic}"
                ))
                total_topics += 1
                
                # 生成该知识点的题目
                questions = generate_chinese_question(grade, topic)
                for q in questions:
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
                    chinese_questions_count += 1
                    total_questions += 1
    
    cursor.executemany(
        "INSERT OR IGNORE INTO topics (subject, grade, name, description) VALUES (?, ?, ?, ?)",
        chinese_topic_data
    )
    conn.commit()
    print(f"  ✓ 导入语文知识点: {len(chinese_topic_data)} 个")
    print(f"  ✓ 生成语文题目: {chinese_questions_count} 道")
    
    print("\n" + "="*60)
    print("数据导入完成！")
    print("="*60)
    print(f"\n统计:")
    print(f"  年级范围: 小学二年级 ~ 小学六年级")
    print(f"  数学知识点: {len(math_topic_data)} 个")
    print(f"  语文知识点: {len(chinese_topic_data)} 个")
    print(f"  数学题目: {total_questions - chinese_questions_count} 道")
    print(f"  语文题目: {chinese_questions_count} 道")
    print(f"  总计: {total_topics} 个知识点, {total_questions} 道题目")

# ========== 查询函数 ==========
def show_summary():
    print("\n" + "="*60)
    print("数据库概览")
    print("="*60)
    
    # 统计各年级知识点
    grades = ["小学二年级", "小学三年级", "小学四年级", "小学五年级", "小学六年级"]
    
    for grade in grades:
        math_topics = db.get_topics(subject="数学", grade=grade)
        chinese_topics = db.get_topics(subject="语文", grade=grade)
        print(f"\n{grade}:")
        print(f"  数学: {len(math_topics)} 个知识点")
        print(f"  语文: {len(chinese_topics)} 个知识点")
    
    # 统计总题目数
    conn = db._get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM topics")
    total_topics = cursor.fetchone()[0]
    
    print("\n" + "="*60)
    print(f"总计: {total_topics} 个知识点, {total_questions} 道题目")
    print("="*60)

if __name__ == "__main__":
    import_all_data()
    show_summary()
