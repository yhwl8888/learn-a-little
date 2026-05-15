import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import threading

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "education.db"

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.local = threading.local()
        self._init_db()
    
    def _get_connection(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
        return self.local.conn
    
    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                grade TEXT NOT NULL,
                avatar TEXT DEFAULT '🧒',
                points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                streak INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                total_questions INTEGER DEFAULT 0,
                correct_questions INTEGER DEFAULT 0,
                study_time INTEGER DEFAULT 0,
                completed_topics TEXT DEFAULT '[]',
                weak_points TEXT DEFAULT '[]',
                strong_points TEXT DEFAULT '[]',
                achievements TEXT DEFAULT '[]',
                date TEXT NOT NULL,
                FOREIGN KEY (child_id) REFERENCES children(id),
                UNIQUE(child_id, date)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wrong_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                your_answer TEXT,
                correct_answer TEXT NOT NULL,
                subject TEXT,
                topic TEXT,
                difficulty INTEGER DEFAULT 1,
                reviewed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER,
                title TEXT NOT NULL,
                category TEXT,
                content TEXT,
                tags TEXT DEFAULT '[]',
                difficulty INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS poems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                dynasty TEXT,
                content TEXT NOT NULL,
                category TEXT,
                difficulty INTEGER DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                grade TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                UNIQUE(subject, grade, name)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                grade TEXT NOT NULL,
                topic TEXT,
                question_type TEXT NOT NULL,
                question_text TEXT NOT NULL,
                answer TEXT NOT NULL,
                explanation TEXT,
                difficulty INTEGER DEFAULT 1,
                options TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                achievement_id TEXT NOT NULL,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id),
                UNIQUE(child_id, achievement_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER NOT NULL,
                subject TEXT,
                questions_count INTEGER DEFAULT 0,
                correct_count INTEGER DEFAULT 0,
                duration INTEGER DEFAULT 0,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_id INTEGER,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                file_type TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            )
        ''')
        
        conn.commit()
        self._seed_data()
    
    def _seed_data(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM children")
        if cursor.fetchone()[0] == 0:
            children = [
                ("大宝", "高三", "🎓", 1250, 8, 15),
                ("二宝", "学前", "🧒", 580, 4, 7)
            ]
            cursor.executemany(
                "INSERT INTO children (name, grade, avatar, points, level, streak) VALUES (?, ?, ?, ?, ?, ?)",
                children
            )
        
        cursor.execute("SELECT COUNT(*) FROM poems")
        if cursor.fetchone()[0] == 0:
            poems = [
                ("春晓", "孟浩然", "唐", "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。", "写景", 1),
                ("静夜思", "李白", "唐", "床前明月光，疑是地上霜。举头望明月，低头思故乡。", "思乡", 1),
                ("登鹳雀楼", "王之涣", "唐", "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。", "哲理", 1),
                ("悯农", "李绅", "唐", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。", "咏物", 1),
                ("咏鹅", "骆宾王", "唐", "鹅鹅鹅，曲项向天歌。白毛浮绿水，红掌拨清波。", "咏物", 1),
                ("江雪", "柳宗元", "唐", "千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。", "写景", 2),
                ("寻隐者不遇", "贾岛", "唐", "松下问童子，言师采药去。只在此山中，云深不知处。", "叙事", 2),
                ("枫桥夜泊", "张继", "唐", "月落乌啼霜满天，江枫渔火对愁眠。姑苏城外寒山寺，夜半钟声到客船。", "羁旅", 2),
                ("游子吟", "孟郊", "唐", "慈母手中线，游子身上衣。临行密密缝，意恐迟迟归。谁言寸草心，报得三春晖。", "亲情", 2),
                ("望庐山瀑布", "李白", "唐", "日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。", "写景", 2),
                ("绝句", "杜甫", "唐", "两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。", "写景", 2),
                ("清明", "杜牧", "唐", "清明时节雨纷纷，路上行人欲断魂。借问酒家何处有，牧童遥指杏花村。", "写景", 2),
                ("黄鹤楼送孟浩然之广陵", "李白", "唐", "故人西辞黄鹤楼，烟花三月下扬州。孤帆远影碧空尽，唯见长江天际流。", "送别", 3),
                ("出塞", "王昌龄", "唐", "秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度阴山。", "边塞", 3),
                ("回乡偶书", "贺知章", "唐", "少小离家老大回，乡音无改鬓毛衰。儿童相见不相识，笑问客从何处来。", "思乡", 2),
            ]
            cursor.executemany(
                "INSERT INTO poems (title, author, dynasty, content, category, difficulty) VALUES (?, ?, ?, ?, ?, ?)",
                poems
            )
        
        cursor.execute("SELECT COUNT(*) FROM topics")
        if cursor.fetchone()[0] == 0:
            topics_data = []
            math_topics = {
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
            }
            
            for grade, topics in math_topics.items():
                for topic in topics:
                    topics_data.append(("数学", grade, topic, f"{grade}{topic}学习"))
            
            chinese_topics = {
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
            }
            
            for grade, topics in chinese_topics.items():
                for topic in topics:
                    topics_data.append(("语文", grade, topic, f"{grade}{topic}学习"))
            
            english_topics = {
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
            
            for grade, topics in english_topics.items():
                for topic in topics:
                    topics_data.append(("英语", grade, topic, f"{grade}{topic}学习"))
            
            cursor.executemany(
                "INSERT OR IGNORE INTO topics (subject, grade, name, description) VALUES (?, ?, ?, ?)",
                topics_data
            )
        
        conn.commit()
    
    def get_children(self) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM children ORDER BY id")
        return [dict(row) for row in cursor.fetchall()]
    
    def add_child(self, name: str, grade: str, avatar: str = "🧒") -> Dict:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO children (name, grade, avatar) VALUES (?, ?, ?)",
            (name, grade, avatar)
        )
        conn.commit()
        return self.get_child(cursor.lastrowid)
    
    def get_child(self, child_id: int) -> Optional[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM children WHERE id = ?", (child_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_child(self, child_id: int, **kwargs) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        valid_fields = ['name', 'grade', 'avatar', 'points', 'level', 'streak']
        updates = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not updates:
            return False
        
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [child_id]
        
        cursor.execute(
            f"UPDATE children SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    
    def add_wrong_question(self, child_id: int, question: str, your_answer: str, 
                          correct_answer: str, subject: str = None, topic: str = None,
                          difficulty: int = 1) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO wrong_questions 
               (child_id, question, your_answer, correct_answer, subject, topic, difficulty)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (child_id, question, your_answer, correct_answer, subject, topic, difficulty)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_wrong_questions(self, child_id: int, reviewed: bool = None) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if reviewed is None:
            cursor.execute(
                "SELECT * FROM wrong_questions WHERE child_id = ? ORDER BY created_at DESC",
                (child_id,)
            )
        else:
            cursor.execute(
                "SELECT * FROM wrong_questions WHERE child_id = ? AND reviewed = ? ORDER BY created_at DESC",
                (child_id, int(reviewed))
            )
        
        return [dict(row) for row in cursor.fetchall()]
    
    def mark_wrong_question_reviewed(self, question_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE wrong_questions SET reviewed = 1 WHERE id = ?",
            (question_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    
    def update_learning_progress(self, child_id: int, date: str = None, **kwargs):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id FROM learning_progress WHERE child_id = ? AND date = ?",
            (child_id, date)
        )
        
        if cursor.fetchone():
            valid_fields = ['total_questions', 'correct_questions', 'study_time', 
                          'completed_topics', 'weak_points', 'strong_points', 'achievements']
            updates = {k: v for k, v in kwargs.items() if k in valid_fields}
            
            for k in ['completed_topics', 'weak_points', 'strong_points', 'achievements']:
                if k in updates and isinstance(updates[k], list):
                    updates[k] = json.dumps(updates[k], ensure_ascii=False)
            
            if updates:
                set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [child_id, date]
                cursor.execute(
                    f"UPDATE learning_progress SET {set_clause} WHERE child_id = ? AND date = ?",
                    values
                )
        else:
            cursor.execute(
                """INSERT INTO learning_progress 
                   (child_id, date, total_questions, correct_questions, study_time,
                    completed_topics, weak_points, strong_points, achievements)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (child_id, date, 
                 kwargs.get('total_questions', 0),
                 kwargs.get('correct_questions', 0),
                 kwargs.get('study_time', 0),
                 json.dumps(kwargs.get('completed_topics', []), ensure_ascii=False),
                 json.dumps(kwargs.get('weak_points', []), ensure_ascii=False),
                 json.dumps(kwargs.get('strong_points', []), ensure_ascii=False),
                 json.dumps(kwargs.get('achievements', []), ensure_ascii=False))
            )
        
        conn.commit()
    
    def get_learning_progress(self, child_id: int, date: str = None) -> Dict:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if date:
            cursor.execute(
                "SELECT * FROM learning_progress WHERE child_id = ? AND date = ?",
                (child_id, date)
            )
        else:
            cursor.execute(
                "SELECT * FROM learning_progress WHERE child_id = ? ORDER BY date DESC LIMIT 1",
                (child_id,)
            )
        
        row = cursor.fetchone()
        if row:
            data = dict(row)
            for k in ['completed_topics', 'weak_points', 'strong_points', 'achievements']:
                if data.get(k):
                    try:
                        data[k] = json.loads(data[k])
                    except:
                        data[k] = []
            return data
        
        return {
            'total_questions': 0,
            'correct_questions': 0,
            'study_time': 0,
            'completed_topics': [],
            'weak_points': [],
            'strong_points': [],
            'achievements': []
        }
    
    def add_achievement(self, child_id: int, achievement_id: str) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO achievements (child_id, achievement_id) VALUES (?, ?)",
                (child_id, achievement_id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_achievements(self, child_id: int) -> List[str]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT achievement_id FROM achievements WHERE child_id = ?",
            (child_id,)
        )
        return [row[0] for row in cursor.fetchall()]
    
    def get_poems(self, category: str = None, difficulty: int = None) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM poems"
        params = []
        conditions = []
        
        if category:
            conditions.append("category = ?")
            params.append(category)
        if difficulty:
            conditions.append("difficulty = ?")
            params.append(difficulty)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_topics(self, subject: str = None, grade: str = None) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM topics"
        params = []
        conditions = []
        
        if subject:
            conditions.append("subject = ?")
            params.append(subject)
        if grade:
            conditions.append("grade = ?")
            params.append(grade)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def add_question(self, subject: str, grade: str, question_type: str, 
                    question_text: str, answer: str, topic: str = None,
                    explanation: str = None, difficulty: int = 1, options: List[str] = None) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        options_json = json.dumps(options, ensure_ascii=False) if options else None
        
        cursor.execute(
            """INSERT INTO questions 
               (subject, grade, topic, question_type, question_text, answer, explanation, difficulty, options)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (subject, grade, topic, question_type, question_text, answer, explanation, difficulty, options_json)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_questions(self, subject: str = None, grade: str = None, 
                     topic: str = None, limit: int = 10) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM questions"
        params = []
        conditions = []
        
        if subject:
            conditions.append("subject = ?")
            params.append(subject)
        if grade:
            conditions.append("grade = ?")
            params.append(grade)
        if topic:
            conditions.append("topic = ?")
            params.append(topic)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY RANDOM() LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        questions = []
        for row in cursor.fetchall():
            q = dict(row)
            if q.get('options'):
                try:
                    q['options'] = json.loads(q['options'])
                except:
                    pass
            questions.append(q)
        
        return questions
    
    def add_study_record(self, child_id: int, subject: str, questions_count: int,
                        correct_count: int, duration: int, date: str = None) -> int:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO study_records 
               (child_id, subject, questions_count, correct_count, duration, date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (child_id, subject, questions_count, correct_count, duration, date)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_study_records(self, child_id: int, days: int = 7) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT * FROM study_records 
               WHERE child_id = ? 
               AND date >= date('now', ?)
               ORDER BY date DESC""",
            (child_id, f'-{days} days')
        )
        
        return [dict(row) for row in cursor.fetchall()]
    
    def add_file(self, child_id: int, filename: str, file_path: str, 
                file_size: int, file_type: str) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO files (child_id, filename, file_path, file_size, file_type) VALUES (?, ?, ?, ?, ?)",
            (child_id, filename, file_path, file_size, file_type)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_files(self, child_id: int) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM files WHERE child_id = ? ORDER BY uploaded_at DESC",
            (child_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        if hasattr(self.local, 'conn'):
            self.local.conn.close()

db = Database()
