#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整教材数据导入脚本
包含小学1-6年级数学、语文，以及3-6年级沪教英语
"""

import random
from database import db

# ========== 各年级数学知识点 ==========
ALL_MATH_TOPICS = {
    "小学一年级": {
        "chapters": [
            {"name": "准备课", "topics": ["数一数", "比多少"]},
            {"name": "位置", "topics": ["上、下、前、后", "左、右"]},
            {"name": "1-5的认识和加减法", "topics": ["1-5的认识", "比大小", "第几", "分与合", "加法", "减法", "0的认识"]},
            {"name": "认识图形（一）", "topics": ["认识立体图形", "拼搭图形"]},
            {"name": "6-10的认识和加减法", "topics": ["6和7的认识", "8和9的认识", "10的认识", "连加、连减", "加减混合"]},
            {"name": "11-20各数的认识", "topics": ["11-20各数的认识", "20以内的进位加法"]},
            {"name": "认识钟表", "topics": ["认识钟表"]},
            {"name": "20以内的退位减法", "topics": ["十几减9", "十几减8、7、6", "十几减5、4、3、2"]},
            {"name": "认识人民币", "topics": ["认识人民币", "简单的计算"]},
            {"name": "找规律", "topics": ["找规律"]}
        ]
    },
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

# ========== 各年级语文知识点 ==========
ALL_CHINESE_TOPICS = {
    "小学一年级": {
        "chapters": [
            {"name": "汉语拼音", "topics": ["a o e", "i u ü y w", "b p m f", "d t n l", "g k h", "j q x", "z c s", "zh ch sh r", "ai ei ui", "ao ou iu", "ie üe er", "an en in un ün", "ang eng ing ong"]},
            {"name": "识字（一）", "topics": ["天地人", "金木水火土", "口耳目", "日月水火", "对韵歌"]},
            {"name": "课文（一）", "topics": ["秋天", "小小的船", "江南", "四季"]},
            {"name": "识字（二）", "topics": ["画", "大小多少", "小书包", "日月明", "升国旗"]},
            {"name": "课文（二）", "topics": ["影子", "比尾巴", "青蛙写诗", "雨点儿", "明天要远足", "大还是小", "项链"]}
        ]
    },
    "小学二年级": {
        "chapters": [
            {"name": "课文", "topics": ["小蝌蚪找妈妈", "我是什么", "植物妈妈有办法", "曹冲称象", "玲玲的画", "一封信", "妈妈睡了", "古诗二首", "黄山奇石", "日月潭", "葡萄沟", "坐井观天", "寒号鸟", "我要的是葫芦"]},
            {"name": "识字", "topics": ["场景歌", "树之歌", "拍手歌", "田家四季歌"]},
            {"name": "语文园地", "topics": ["口语交际", "写话", "日积月累"]}
        ]
    },
    "小学三年级": {
        "chapters": [
            {"name": "课文", "topics": ["大青树下的小学", "花的学校", "不懂就要问", "古诗三首", "秋天的雨", "听听，秋的声音", "卖火柴的小女孩", "那一定会很好", "在牛肚子里旅行", "一块奶酪", "总也倒不了的老屋", "胡萝卜先生的长胡子", "小狗学叫"]},
            {"name": "写作", "topics": ["写日记", "我来编童话", "续写故事", "我们眼中的缤纷世界", "这儿真美", "那次玩得真高兴"]},
            {"name": "古诗", "topics": ["山行", "赠刘景文", "夜书所见", "望天门山", "饮湖上初晴后雨", "望洞庭"]}
        ]
    },
    "小学四年级": {
        "chapters": [
            {"name": "课文", "topics": ["观潮", "走月亮", "现代诗二首", "繁星", "一个豆荚里的五粒豆", "蝙蝠和雷达", "呼风唤雨的世纪", "蝴蝶的家", "古诗三首", "爬山虎的脚", "蟋蟀的住宅", "盘古开天地", "精卫填海", "普罗米修斯", "女娲补天", "麻雀", "爬天都峰"]},
            {"name": "写作", "topics": ["写观察日记", "写童话", "写绿豆", "写小动物", "写导游词", "写信", "我的心儿怦怦跳"]},
            {"name": "古诗", "topics": ["暮江吟", "题西林壁", "雪梅", "出塞", "凉州词", "夏日绝句", "别董大"]}
        ]
    },
    "小学五年级": {
        "chapters": [
            {"name": "课文", "topics": ["白鹭", "落花生", "桂花雨", "珍珠鸟", "搭石", "将相和", "什么比猎豹的速度更快", "冀中的地道战", "猎人海力布", "牛郎织女", "父爱之舟", "精彩极了和糟糕透了", "圆明园的毁灭", "七律·长征", "狼牙山五壮士", "开国大典", "灯光", "松鼠", "慈母情深"]},
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

# ========== 3-6年级沪教英语知识点 ==========
ALL_ENGLISH_TOPICS = {
    "小学三年级": {
        "chapters": [
            {"name": "Module 1", "topics": ["Greetings", "Introductions", "Hello and Goodbye", "What's your name?"]},
            {"name": "Module 2", "topics": ["Family members", "Who is he/she?", "This is my mother", "My family"]},
            {"name": "Module 3", "topics": ["Colors", "What color is it?", "Red, blue, green", "I like colors"]},
            {"name": "Module 4", "topics": ["Numbers 1-10", "How many?", "Counting", "Numbers and counting"]},
            {"name": "Module 5", "topics": ["Classroom", "What's this?", "It's a...", "In the classroom"]},
            {"name": "Module 6", "topics": ["Animals", "What is it?", "It's a dog", "I like animals"]}
        ]
    },
    "小学四年级": {
        "chapters": [
            {"name": "Module 1", "topics": ["Daily activities", "What do you do?", "I play football", "My day"]},
            {"name": "Module 2", "topics": ["School subjects", "What's your favourite subject?", "I like maths", "Subjects"]},
            {"name": "Module 3", "topics": ["Places", "Where is the library?", "It's on the second floor", "In the school"]},
            {"name": "Module 4", "topics": ["Transportation", "How do you come to school?", "I come by bus", "Transportation"]},
            {"name": "Module 5", "topics": ["Weather", "What's the weather like?", "It's sunny", "Weather and seasons"]},
            {"name": "Module 6", "topics": ["Food and drinks", "What do you like?", "I like juice", "Food"]}
        ]
    },
    "小学五年级": {
        "chapters": [
            {"name": "Module 1", "topics": ["Changes", "What have you changed?", "I've got new shoes", "Changes in life"]},
            {"name": "Module 2", "topics": ["Rules", "What are the rules?", "We must... / Don't...", "School rules"]},
            {"name": "Module 3", "topics": ["Travel", "Where did you go?", "I went to Shanghai", "Holiday plans"]},
            {"name": "Module 4", "topics": ["Hobbies", "What are your hobbies?", "I like collecting stamps", "Free time activities"]},
            {"name": "Module 5", "topics": ["Health", "What should we do?", "We should eat vegetables", "Being healthy"]},
            {"name": "Module 6", "topics": ["The future", "What will you be?", "I will be a teacher", "Future plans"]}
        ]
    },
    "小学六年级": {
        "chapters": [
            {"name": "Module 1", "topics": ["Long ago and now", "What was it like?", "Everything has changed", "Changes over time"]},
            {"name": "Module 2", "topics": ["Work and play", "People and jobs", "Doctors help people", "Jobs and work"]},
            {"name": "Module 3", "topics": ["Places and travel", "Travelling", "I'm going to visit", "Travel plans"]},
            {"name": "Module 4", "topics": ["Friends", "Good friends", "Friends help each other", "Being a good friend"]},
            {"name": "Module 5", "topics": ["Famous people", "Great people", "She was a doctor", "Famous people"]},
            {"name": "Module 6", "topics": ["Revision", "Review of everything", "Consolidation", "Putting it together"]}
        ]
    }
}

# ========== 古诗词库 ==========
POEMS_DATA = [
    {"title": "江南", "author": "汉乐府", "dynasty": "汉", "content": "江南可采莲，莲叶何田田。鱼戏莲叶间。", "category": "古诗", "difficulty": 1},
    {"title": "画", "author": "王维", "dynasty": "唐", "content": "远看山有色，近听水无声。春去花还在，人来鸟不惊。", "category": "古诗", "difficulty": 1},
    {"title": "悯农", "author": "李绅", "dynasty": "唐", "content": "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。", "category": "古诗", "difficulty": 1},
    {"title": "静夜思", "author": "李白", "dynasty": "唐", "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。", "category": "古诗", "difficulty": 1},
    {"title": "登鹳雀楼", "author": "王之涣", "dynasty": "唐", "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。", "category": "古诗", "difficulty": 2},
    {"title": "春晓", "author": "孟浩然", "dynasty": "唐", "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。", "category": "古诗", "difficulty": 1},
    {"title": "望庐山瀑布", "author": "李白", "dynasty": "唐", "content": "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。", "category": "古诗", "difficulty": 2},
    {"title": "山行", "author": "杜牧", "dynasty": "唐", "content": "远上寒山石径斜，白云生处有人家。停车坐爱枫林晚，霜叶红于二月花。", "category": "古诗", "difficulty": 2},
    {"title": "赠刘景文", "author": "苏轼", "dynasty": "宋", "content": "荷尽已无擎雨盖，菊残犹有傲霜枝。一年好景君须记，正是橙黄橘绿时。", "category": "古诗", "difficulty": 2},
    {"title": "夜书所见", "author": "叶绍翁", "dynasty": "宋", "content": "萧萧梧叶送寒声，江上秋风动客情。知有儿童挑促织，夜深篱落一灯明。", "category": "古诗", "difficulty": 2},
    {"title": "望天门山", "author": "李白", "dynasty": "唐", "content": "天门中断楚江开，碧水东流至此回。两岸青山相对出，孤帆一片日边来。", "category": "古诗", "difficulty": 2},
    {"title": "饮湖上初晴后雨", "author": "苏轼", "dynasty": "宋", "content": "水光潋滟晴方好，山色空蒙雨亦奇。欲把西湖比西子，淡妆浓抹总相宜。", "category": "古诗", "difficulty": 2},
    {"title": "望洞庭", "author": "刘禹锡", "dynasty": "唐", "content": "湖光秋月两相和，潭面无风镜未磨。遥望洞庭山水翠，白银盘里一青螺。", "category": "古诗", "difficulty": 2},
    {"title": "暮江吟", "author": "白居易", "dynasty": "唐", "content": "一道残阳铺水中，半江瑟瑟半江红。可怜九月初三夜，露似真珠月似弓。", "category": "古诗", "difficulty": 2},
    {"title": "题西林壁", "author": "苏轼", "dynasty": "宋", "content": "横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。", "category": "古诗", "difficulty": 2},
    {"title": "雪梅", "author": "卢梅坡", "dynasty": "宋", "content": "梅雪争春未肯降，骚人搁笔费评章。梅须逊雪三分白，雪却输梅一段香。", "category": "古诗", "difficulty": 2},
    {"title": "出塞", "author": "王昌龄", "dynasty": "唐", "content": "秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度阴山。", "category": "古诗", "difficulty": 3},
    {"title": "凉州词", "author": "王翰", "dynasty": "唐", "content": "葡萄美酒夜光杯，欲饮琵琶马上催。醉卧沙场君莫笑，古来征战几人回。", "category": "古诗", "difficulty": 3},
    {"title": "夏日绝句", "author": "李清照", "dynasty": "宋", "content": "生当作人杰，死亦为鬼雄。至今思项羽，不肯过江东。", "category": "古诗", "difficulty": 2},
    {"title": "示儿", "author": "陆游", "dynasty": "宋", "content": "死去元知万事空，但悲不见九州同。王师北定中原日，家祭无忘告乃翁。", "category": "古诗", "difficulty": 3},
    {"title": "题临安邸", "author": "林升", "dynasty": "宋", "content": "山外青山楼外楼，西湖歌舞几时休？暖风熏得游人醉，直把杭州作汴州。", "category": "古诗", "difficulty": 3},
    {"title": "已亥杂诗", "author": "龚自珍", "dynasty": "清", "content": "九州生气恃风雷，万马齐喑究可哀。我劝天公重抖擞，不拘一格降人才。", "category": "古诗", "difficulty": 3},
    {"title": "山居秋暝", "author": "王维", "dynasty": "唐", "content": "空山新雨后，天气晚来秋。明月松间照，清泉石上流。", "category": "古诗", "difficulty": 3},
    {"title": "枫桥夜泊", "author": "张继", "dynasty": "唐", "content": "月落乌啼霜满天，江枫渔火对愁眠。姑苏城外寒山寺，夜半钟声到客船。", "category": "古诗", "difficulty": 2},
    {"title": "长相思", "author": "纳兰性德", "dynasty": "清", "content": "山一程，水一程，身向榆关那畔行，夜深千帐灯。", "category": "古词", "difficulty": 3},
]

# ========== 题目生成函数 ==========

def generate_math_questions(grade, topic):
    """生成数学题目"""
    questions = []
    
    # 根据知识点类型生成不同题目
    if "加法" in topic:
        if "两位数" in topic or "100以内" in topic:
            for _ in range(15):
                a = random.randint(10, 99)
                b = random.randint(10, 99)
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
        elif "万以内" in topic:
            for _ in range(12):
                a = random.randint(1000, 9999)
                b = random.randint(100, 999)
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
        elif "小数" in topic:
            for _ in range(10):
                a = round(random.uniform(1, 99), 2)
                b = round(random.uniform(1, 9), 2)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a} + {b} = ?",
                    "answer": f"{a + b:.2f}",
                    "explanation": f"{a} + {b} = {a + b:.2f}",
                    "difficulty": 3
                })
        elif "分数" in topic:
            for _ in range(8):
                a, b = random.randint(1, 9), random.randint(1, 9)
                c, d = random.randint(1, 9), random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a}/{b} + {c}/{d} = ?",
                    "answer": f"{a*d + b*c}/{b*d}",
                    "explanation": f"异分母分数加法：先通分再相加",
                    "difficulty": 3
                })
    
    elif "减法" in topic:
        if "两位数" in topic or "100以内" in topic:
            for _ in range(15):
                a = random.randint(50, 99)
                b = random.randint(10, a)
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
            for _ in range(12):
                a = random.randint(5000, 9999)
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
        if "一位数" in topic:
            for _ in range(15):
                a = random.randint(10, 999)
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
        elif "两位数" in topic:
            for _ in range(12):
                a = random.randint(10, 99)
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
        elif "分数" in topic:
            for _ in range(10):
                a, b = random.randint(1, 9), random.randint(1, 9)
                c, d = random.randint(1, 9), random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a}/{b} × {c}/{d} = ?",
                    "answer": f"{a*c}/{b*d}",
                    "explanation": f"分数乘法：分子乘分子，分母乘分母",
                    "difficulty": 3
                })
        elif "口诀" in topic:
            num = random.randint(2, 9)
            for _ in range(8):
                multiplier = random.randint(1, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "口算题",
                    "question_text": f"{num} × {multiplier} = ?",
                    "answer": str(num * multiplier),
                    "explanation": f"运用乘法口诀：{num}的乘法口诀",
                    "difficulty": 2
                })
    
    elif "除法" in topic:
        if "整数" in topic or "两位数除以一位数" in topic:
            for _ in range(15):
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
        elif "两位数" in topic:
            for _ in range(12):
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
        elif "分数" in topic:
            for _ in range(10):
                a, b = random.randint(1, 9), random.randint(2, 9)
                c, d = random.randint(1, 9), random.randint(2, 9)
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "计算题",
                    "question_text": f"{a}/{b} ÷ {c}/{d} = ?",
                    "answer": f"{a*d}/{b*c}",
                    "explanation": f"分数除法：乘以倒数",
                    "difficulty": 3
                })
    
    elif "小数" in topic:
        for _ in range(10):
            a = round(random.uniform(1, 99), 2)
            b = random.randint(1, 9)
            questions.append({
                "subject": "数学",
                "grade": grade,
                "topic": topic,
                "question_type": "计算题",
                "question_text": f"{a} × {b} = ? (保留两位小数)",
                "answer": f"{a * b:.2f}",
                "explanation": f"{a} × {b} = {a * b:.2f}",
                "difficulty": 3
            })
    
    elif "周长" in topic or "面积" in topic:
        for _ in range(8):
            length = random.randint(2, 20)
            width = random.randint(2, 20)
            if "周长" in topic:
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "应用题",
                    "question_text": f"一个长方形，长{length}厘米，宽{width}厘米，周长是多少厘米？",
                    "answer": str((length + width) * 2),
                    "explanation": f"周长 = (长 + 宽) × 2 = ({length} + {width}) × 2 = {(length + width) * 2}厘米",
                    "difficulty": 2
                })
            else:
                questions.append({
                    "subject": "数学",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "应用题",
                    "question_text": f"一个长方形，长{length}厘米，宽{width}厘米，面积是多少平方厘米？",
                    "answer": str(length * width),
                    "explanation": f"面积 = 长 × 宽 = {length} × {width} = {length * width}平方厘米",
                    "difficulty": 2
                })
    
    elif "分数" in topic:
        for _ in range(8):
            a, b = random.randint(1, 9), random.randint(2, 9)
            questions.append({
                "subject": "数学",
                "grade": grade,
                "topic": topic,
                "question_type": "填空题",
                "question_text": f"{a}/{b} 这个分数，分子是{a}，分母是{b}，表示{a}÷{b}。",
                "answer": "正确",
                "explanation": f"分数表示分子除以分母",
                "difficulty": 2
            })
    
    else:
        # 默认生成一些基础题目
        for _ in range(5):
            a, b = random.randint(10, 99), random.randint(1, 9)
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
    
    return questions

def generate_chinese_questions(grade, topic):
    """生成语文题目"""
    questions = []
    
    # 古诗词相关
    if "古诗" in topic or "诗词" in topic or "古词" in topic:
        poems = [p for p in POEMS_DATA if p["difficulty"] <= (3 if "五" in grade or "六" in grade else 2)]
        
        for poem in poems[:3]:
            # 诗句填空
            lines = poem["content"].replace("，", " ").replace("。", " ").split()
            for line in lines[:2]:
                words = list(line)
                if len(words) >= 4:
                    idx = random.randint(2, len(words) - 2)
                    q = "".join(words[:idx]) + "____" + "".join(words[idx+1:])
                    questions.append({
                        "subject": "语文",
                        "grade": grade,
                        "topic": topic,
                        "question_type": "古诗填空",
                        "question_text": f"《{poem['title']}》 - {poem['author']}\n{q}",
                        "answer": words[idx],
                        "explanation": f"出自{poem['author']}的《{poem['title']}》",
                        "difficulty": 2
                    })
            
            # 理解题
            questions.append({
                "subject": "语文",
                "grade": grade,
                "topic": topic,
                "question_type": "古诗理解",
                "question_text": f"《{poem['title']}》这首诗表达了诗人什么样的情感？",
                "answer": "借景抒情",
                "explanation": f"《{poem['title']}》通过景物描写来表达诗人情感",
                "difficulty": 3
            })
    
    # 文言文相关
    elif "文言文" in topic or "伯牙" in topic or "学弈" in topic or "两小儿" in topic:
        questions.append({
            "subject": "语文",
            "grade": grade,
            "topic": topic,
            "question_type": "文言文理解",
            "question_text": '解释"之"字在不同语境中的用法',
            "answer": "助词，的；代词，他（它）；动词，到",
            "explanation": "之字在文言文中有多种用法",
            "difficulty": 3
        })
        questions.append({
            "subject": "语文",
            "grade": grade,
            "topic": topic,
            "question_type": "文言文翻译",
            "question_text": "翻译：学弈",
            "answer": "学习下棋",
            "explanation": "这篇文言文讲述了学习下棋的道理",
            "difficulty": 3
        })
    
    # 课文理解
    elif "课文" in topic:
        # 近义词
        antonyms = [("高", "低"), ("远", "近"), ("快", "慢"), ("容易", "困难"), ("打开", "关闭")]
        for word, antonym in antonyms[:2]:
            questions.append({
                "subject": "语文",
                "grade": grade,
                "topic": topic,
                "question_type": "词语理解",
                "question_text": f'写出"{word}"的反义词',
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
            "question_text": "判断修辞：荷叶像一个个碧绿的大圆盘。",
            "answer": "比喻",
            "explanation": "把荷叶比作大圆盘，是比喻中的明喻",
            "difficulty": 2
        })
    
    # 写作相关
    elif "写作" in topic or "写话" in topic:
        questions.append({
            "subject": "语文",
            "grade": grade,
            "topic": topic,
            "question_type": "写作题",
            "question_text": "请根据题目写一段话，注意条理清晰，不少于100字。",
            "answer": "开放题",
            "explanation": "考查写作能力",
            "difficulty": 3
        })
    
    else:
        # 默认题目
        for _ in range(3):
            questions.append({
                "subject": "语文",
                "grade": grade,
                "topic": topic,
                "question_type": "理解题",
                "question_text": f"理解并掌握本课的生字词",
                "answer": "略",
                "explanation": "学习重点词汇和表达",
                "difficulty": 2
            })
    
    return questions

def generate_english_questions(grade, topic):
    """生成英语题目"""
    questions = []
    
    # 词汇题
    vocabularies = {
        "Greetings": [("Hello", "你好"), ("Goodbye", "再见"), ("Good morning", "早上好"), ("Thank you", "谢谢")],
        "Family members": [("mother", "妈妈"), ("father", "爸爸"), ("sister", "姐姐/妹妹"), ("brother", "哥哥/弟弟")],
        "Colors": [("red", "红色"), ("blue", "蓝色"), ("green", "绿色"), ("yellow", "黄色")],
        "Numbers": [("one", "一"), ("two", "二"), ("three", "三"), ("four", "四"), ("five", "五")],
        "Classroom": [("desk", "桌子"), ("chair", "椅子"), ("blackboard", "黑板"), ("book", "书")],
        "Animals": [("dog", "狗"), ("cat", "猫"), ("bird", "鸟"), ("fish", "鱼")],
        "Food": [("apple", "苹果"), ("banana", "香蕉"), ("orange", "橙子"), ("milk", "牛奶")],
        "Drinks": [("water", "水"), ("juice", "果汁"), ("tea", "茶"), ("coffee", "咖啡")],
        "Weather": [("sunny", "晴朗的"), ("rainy", "下雨的"), ("cloudy", "多云的"), ("windy", "有风的")],
        "School subjects": [("maths", "数学"), ("English", "英语"), ("Chinese", "语文"), ("PE", "体育")],
    }
    
    # 根据话题生成题目
    topic_lower = topic.lower()
    
    # 单词拼写
    for key, words in vocabularies.items():
        if any(word.lower() in topic_lower for word in key.split()):
            for english, chinese in words[:3]:
                questions.append({
                    "subject": "英语",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "词汇题",
                    "question_text": f"单词拼写：{chinese}",
                    "answer": english,
                    "explanation": f"{chinese} 的英语是 {english}",
                    "difficulty": 1
                })
                questions.append({
                    "subject": "英语",
                    "grade": grade,
                    "topic": topic,
                    "question_type": "翻译题",
                    "question_text": f"翻译：{english}",
                    "answer": chinese,
                    "explanation": f"{english} 的意思是 {chinese}",
                    "difficulty": 1
                })
    
    # 句型练习
    if "what" in topic_lower or "name" in topic_lower:
        questions.append({
            "subject": "英语",
            "grade": grade,
            "topic": topic,
            "question_type": "句型题",
            "question_text": "What's your name?（回答问题）",
            "answer": "My name is...",
            "explanation": "回答：我的名字是...",
            "difficulty": 1
        })
    
    if "how many" in topic_lower or "counting" in topic_lower or "numbers" in topic_lower:
        questions.append({
            "subject": "英语",
            "grade": grade,
            "topic": topic,
            "question_type": "问答配对",
            "question_text": "How many books are there? - There are three books.",
            "answer": "正确",
            "explanation": "How many 引导的特殊疑问句回答数量",
            "difficulty": 1
        })
    
    if "family" in topic_lower:
        questions.append({
            "subject": "英语",
            "grade": grade,
            "topic": topic,
            "question_type": "句型题",
            "question_text": "This is my mother.（翻译成英语）",
            "answer": "这是我的妈妈",
            "explanation": "介绍家庭成员用 This is my...",
            "difficulty": 1
        })
    
    if "color" in topic_lower:
        questions.append({
            "subject": "英语",
            "grade": grade,
            "topic": topic,
            "question_type": "句型题",
            "question_text": "What color is it? - It's red.",
            "answer": "正确",
            "explanation": "What color is it? 用于询问颜色",
            "difficulty": 1
        })
    
    if "favorite" in topic_lower or "subject" in topic_lower:
        questions.append({
            "subject": "英语",
            "grade": grade,
            "topic": topic,
            "question_type": "句型题",
            "question_text": "What's your favourite subject?（用英语回答）",
            "answer": "My favourite subject is...",
            "explanation": "回答：我最喜欢的科目是...",
            "difficulty": 2
        })
    
    if "weather" in topic_lower:
        questions.append({
            "subject": "英语",
            "grade": grade,
            "topic": topic,
            "question_type": "句型题",
            "question_text": "What's the weather like today?（回答）",
            "answer": "It's sunny/rainy/cloudy...",
            "explanation": "回答今天的天气状况",
            "difficulty": 2
        })
    
    if "job" in topic_lower or "work" in topic_lower:
        questions.append({
            "subject": "英语",
            "grade": grade,
            "topic": topic,
            "question_type": "职业题",
            "question_text": "What does she do? - She is a doctor.",
            "answer": "正确",
            "explanation": "What does she do? 用于询问职业",
            "difficulty": 2
        })
    
    if "future" in topic_lower or "will" in topic_lower:
        questions.append({
            "subject": "英语",
            "grade": grade,
            "topic": topic,
            "question_type": "时态题",
            "question_text": "I will be a teacher in the future. (翻译)",
            "answer": "将来我会成为一名老师",
            "explanation": "will 表示将来时态",
            "difficulty": 2
        })
    
    # 如果没有生成题目，添加一些基础题目
    if not questions:
        for _ in range(5):
            questions.append({
                "subject": "英语",
                "grade": grade,
                "topic": topic,
                "question_type": "词汇题",
                "question_text": f"学习本课重点词汇和句型",
                "answer": "略",
                "explanation": "掌握本课内容",
                "difficulty": 1
            })
    
    return questions

# ========== 数据导入主函数 ==========
def import_all_data():
    print("=" * 70)
    print("开始导入完整教材数据")
    print("=" * 70)
    
    conn = db._get_connection()
    cursor = conn.cursor()
    
    stats = {
        "math_topics": 0,
        "math_questions": 0,
        "chinese_topics": 0,
        "chinese_questions": 0,
        "english_topics": 0,
        "english_questions": 0,
        "poems": 0
    }
    
    # 1. 导入数学知识点和题目
    print("\n【1】导入数学教材数据（1-6年级）...")
    for grade, data in ALL_MATH_TOPICS.items():
        for chapter in data["chapters"]:
            chapter_name = chapter["name"]
            for topic in chapter["topics"]:
                cursor.execute(
                    "INSERT OR IGNORE INTO topics (subject, grade, name, description) VALUES (?, ?, ?, ?)",
                    ("数学", grade, topic, f"{chapter_name} - {topic}")
                )
                stats["math_topics"] += 1
                
                # 生成题目
                questions = generate_math_questions(grade, topic)
                for q in questions:
                    db.add_question(**q)
                    stats["math_questions"] += 1
    
    conn.commit()
    print(f"  ✓ 数学知识点: {stats['math_topics']} 个")
    print(f"  ✓ 数学题目: {stats['math_questions']} 道")
    
    # 2. 导入语文知识点和题目
    print("\n【2】导入语文教材数据（1-6年级）...")
    for grade, data in ALL_CHINESE_TOPICS.items():
        for chapter in data["chapters"]:
            chapter_name = chapter["name"]
            for topic in chapter["topics"]:
                cursor.execute(
                    "INSERT OR IGNORE INTO topics (subject, grade, name, description) VALUES (?, ?, ?, ?)",
                    ("语文", grade, topic, f"{chapter_name} - {topic}")
                )
                stats["chinese_topics"] += 1
                
                # 生成题目
                questions = generate_chinese_questions(grade, topic)
                for q in questions:
                    db.add_question(**q)
                    stats["chinese_questions"] += 1
    
    conn.commit()
    print(f"  ✓ 语文知识点: {stats['chinese_topics']} 个")
    print(f"  ✓ 语文题目: {stats['chinese_questions']} 道")
    
    # 3. 导入英语知识点和题目（3-6年级）
    print("\n【3】导入英语教材数据（3-6年级沪教英语）...")
    for grade, data in ALL_ENGLISH_TOPICS.items():
        for chapter in data["chapters"]:
            chapter_name = chapter["name"]
            for topic in chapter["topics"]:
                cursor.execute(
                    "INSERT OR IGNORE INTO topics (subject, grade, name, description) VALUES (?, ?, ?, ?)",
                    ("英语", grade, topic, f"{chapter_name} - {topic}")
                )
                stats["english_topics"] += 1
                
                # 生成题目
                questions = generate_english_questions(grade, topic)
                for q in questions:
                    db.add_question(**q)
                    stats["english_questions"] += 1
    
    conn.commit()
    print(f"  ✓ 英语知识点: {stats['english_topics']} 个")
    print(f"  ✓ 英语题目: {stats['english_questions']} 道")
    
    # 4. 导入古诗词
    print("\n【4】导入古诗词库...")
    for poem in POEMS_DATA:
        cursor.execute(
            "INSERT OR IGNORE INTO poems (title, author, dynasty, content, category, difficulty) VALUES (?, ?, ?, ?, ?, ?)",
            (poem["title"], poem["author"], poem["dynasty"], poem["content"], poem["category"], poem["difficulty"])
        )
        stats["poems"] += 1
    
    conn.commit()
    print(f"  ✓ 古诗词: {stats['poems']} 首")
    
    print("\n" + "=" * 70)
    print("数据导入完成！")
    print("=" * 70)
    
    total_topics = stats["math_topics"] + stats["chinese_topics"] + stats["english_topics"]
    total_questions = stats["math_questions"] + stats["chinese_questions"] + stats["english_questions"]
    
    print(f"\n总计:")
    print(f"  数学知识点: {stats['math_topics']} 个")
    print(f"  语文知识点: {stats['chinese_topics']} 个")
    print(f"  英语知识点: {stats['english_topics']} 个")
    print(f"  古诗词: {stats['poems']} 首")
    print(f"  数学题目: {stats['math_questions']} 道")
    print(f"  语文题目: {stats['chinese_questions']} 道")
    print(f"  英语题目: {stats['english_questions']} 道")
    print(f"\n  知识点总计: {total_topics} 个")
    print(f"  题目总计: {total_questions} 道")
    print("=" * 70)

# ========== 查询和展示函数 ==========
def show_summary():
    print("\n" + "=" * 70)
    print("数据库概览")
    print("=" * 70)
    
    # 按年级统计
    grades = ["小学一年级", "小学二年级", "小学三年级", "小学四年级", "小学五年级", "小学六年级"]
    
    for grade in grades:
        math_topics = db.get_topics(subject="数学", grade=grade)
        chinese_topics = db.get_topics(subject="语文", grade=grade)
        english_topics = db.get_topics(subject="英语", grade=grade)
        
        print(f"\n{grade}:")
        print(f"  数学: {len(math_topics)} 个知识点")
        print(f"  语文: {len(chinese_topics)} 个知识点")
        print(f"  英语: {len(english_topics)} 个知识点")
    
    # 统计总计
    conn = db._get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM topics")
    total_topics = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM poems")
    total_poems = cursor.fetchone()[0]
    
    print("\n" + "=" * 70)
    print(f"总计: {total_topics} 个知识点, {total_questions} 道题目, {total_poems} 首古诗词")
    print("=" * 70)

if __name__ == "__main__":
    import_all_data()
    show_summary()
