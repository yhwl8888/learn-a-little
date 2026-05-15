// 全局状态
let currentChild = 1;
let currentModel = 'qwen2.5:7b-instruct-q4_K_M';
let isProcessing = false;
let chatHistory = []; // 聊天历史
let currentQuestions = []; // 当前生成的题目（用于打印）

// 年级科目映射
const GRADE_SUBJECT_MAP = {
    '小学一年级': ['数学', '语文'],
    '小学二年级': ['数学', '语文'],
    '小学三年级': ['数学', '语文', '英语'],
    '小学四年级': ['数学', '语文', '英语'],
    '小学五年级': ['数学', '语文', '英语'],
    '小学六年级': ['数学', '语文', '英语'],
    '初一': ['数学', '语文', '英语', '生物', '地理', '历史'],
    '初二': ['数学', '语文', '英语', '物理', '生物'],
    '初三': ['数学', '语文', '英语', '物理', '化学'],
    '高一': ['数学', '语文', '英语', '物理', '化学', '生物'],
    '高二': ['数学', '语文', '英语', '物理', '化学', '生物'],
    '高三': ['数学', '语文', '英语', '物理', '化学', '生物']
};

// 初始化
async function init() {
    await loadChildren();
    await loadModels();
    await loadStats();
    updateSubjectOptions();
    document.getElementById('examGrade').addEventListener('change', updateSubjectOptions);
}

// 加载孩子列表
async function loadChildren() {
    try {
        const r = await fetch('/api/children');
        const d = await r.json();
        const select = document.getElementById('childSelect');
        
        if (d.children && d.children.length > 0) {
            select.innerHTML = d.children.map(c => 
                `<option value="${c.id}">${c.name}（${c.grade}）</option>`
            ).join('');
            currentChild = d.children[0].id;
        }
    } catch(e) {
        console.error('加载孩子列表失败', e);
    }
}

// 显示孩子编辑弹窗
function showChildEditor() {
    const select = document.getElementById('childSelect');
    const selectedOption = select.options[select.selectedIndex];
    const text = selectedOption.text;
    
    // 解析当前选中的孩子信息
    const name = text.split('（')[0];
    const grade = text.match(/（(.+)）/)?.[1] || '';
    
    document.getElementById('editChildName').value = name;
    document.getElementById('editChildGrade').value = grade;
    document.getElementById('childModal').style.display = 'flex';
}

// 关闭弹窗
function closeChildModal() {
    document.getElementById('childModal').style.display = 'none';
}

// 保存孩子信息
async function saveChildInfo() {
    const name = document.getElementById('editChildName').value.trim();
    const grade = document.getElementById('editChildGrade').value;
    
    if (!name) {
        alert('请输入昵称');
        return;
    }
    
    try {
        const r = await fetch('/api/children/' + currentChild, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, grade})
        });
        
        const d = await r.json();
        
        if (d.success) {
            // 更新下拉菜单显示
            const select = document.getElementById('childSelect');
            const option = select.options[select.selectedIndex];
            option.text = `${name}（${grade}）`;
            
            closeChildModal();
            alert('保存成功！');
        } else {
            alert('保存失败：' + (d.error || '未知错误'));
        }
    } catch(e) {
        alert('保存失败：' + e.message);
    }
}

// 加载模型列表
async function loadModels() {
    try {
        const r = await fetch('/api/models/list');
        const d = await r.json();
        const select = document.getElementById('modelSelect');
        select.innerHTML = d.models.map(m => {
            // 显示完整名称，区分不同版本
            const displayName = m.name.includes(':') ? m.name : m.name;
            return `<option value="${m.name}">${displayName}</option>`;
        }).join('');
    } catch(e) {
        console.error('加载模型失败', e);
    }
}

// 加载统计数据
async function loadStats() {
    try {
        const r = await fetch('/api/diagnosis?child_id=' + currentChild);
        const d = await r.json();
        
        // 更新诊断页面
        document.getElementById('diagnosisStats').innerHTML = `
            <div class="stat-card"><div class="stat-value">${d.total_questions || 0}</div><div class="stat-label">总题目数</div></div>
            <div class="stat-card"><div class="stat-value">${d.correct_rate || '0%'}</div><div class="stat-label">正确率</div></div>
            <div class="stat-card"><div class="stat-value">${d.wrong_count || 0}</div><div class="stat-label">错题数</div></div>
        `;
        
        // 更新错题统计
        document.getElementById('wrongStats').innerHTML = `
            <div class="stat-card"><div class="stat-value">${d.wrong_count || 0}</div><div class="stat-label">待复习错题</div></div>
        `;
    } catch(e) {
        console.error('加载统计失败', e);
    }
}

// 更新科目选项
function updateSubjectOptions() {
    const grade = document.getElementById('examGrade').value;
    const subjects = GRADE_SUBJECT_MAP[grade] || ['数学', '语文', '英语'];
    const select = document.getElementById('examSubject');
    select.innerHTML = subjects.map(s => `<option value="${s}">${s}</option>`).join('');
}

// 页面切换
function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
    
    document.getElementById(page + 'Page').classList.add('active');
    event.currentTarget.classList.add('active');
    
    const titles = {
        chat: 'AI对话', exam: '智能出题', photo: '拍照批改',
        wrong: '错题本', plan: '学习计划', diagnosis: '诊断报告', knowledge: '知识库'
    };
    document.getElementById('pageTitle').textContent = titles[page];
    
    // 加载页面数据
    if (page === 'diagnosis' || page === 'wrong') loadStats();
    if (page === 'knowledge') loadKnowledge();
}

// 侧边栏切换
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('sidebarOverlay').classList.toggle('show');
}

// 切换孩子
function switchChild(id) {
    currentChild = parseInt(id);
    loadStats();
}

// 切换模型
function switchModel(model) {
    currentModel = model;
}

// 发送消息
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg || isProcessing) return;
    
    // 检查是否是时间/农历查询
    if (/几点|时间|什么时候|农历|几号|星期|日期|今天/.test(msg) && !/故事|讲|写作/.test(msg)) {
        try {
            const r = await fetch('/api/time');
            const info = await r.json();
            const reply = `现在是 ${info.date} ${info.time}，${info.weekday}，${info.lunar}${info.holiday ? '，今天是' + info.holiday : ''}`;
            addMessage('user', msg);
            addMessage('assistant', reply);
        } catch(e) {
            addMessage('user', msg);
            addMessage('assistant', '获取时间失败');
        }
        input.value = '';
        return;
    }
    
    // 检查是否是倒计时查询
    const countdownMatch = msg.match(/距离|离.*(还有|多久)/);
    if (countdownMatch) {
        const targets = ['春节', '元宵', '清明', '劳动节', '端午', '七夕', '中秋', '国庆', '元旦', '除夕'];
        const target = targets.find(t => msg.includes(t));
        if (target) {
            try {
                const r = await fetch(`/api/time/countdown?target=${encodeURIComponent(target)}`);
                const info = await r.json();
                if (info.message) {
                    addMessage('user', msg);
                    addMessage('assistant', info.message);
                    input.value = '';
                    return;
                }
            } catch(e) {}
        }
    }
    
    input.value = '';
    addMessage('user', msg);
    
    // 添加到历史
    chatHistory.push({role: 'user', content: msg});
    
    isProcessing = true;
    
    // 检查是否是节日查询
    const holidayAnswer = checkHolidayQuery(msg);
    if (holidayAnswer) {
        addMessage('assistant', holidayAnswer);
        chatHistory.push({role: 'assistant', content: holidayAnswer});
        isProcessing = false;
        return;
    }
    
    // 检查是否需要调用工具
    const tool = checkTools(msg);
    
    if (tool && tool.type === 'weather') {
        const result = await getWeather(tool.city, tool.isTomorrow);
        if (result) {
            addMessage('assistant', result);
            chatHistory.push({role: 'assistant', content: result});
            isProcessing = false;
            return;
        }
    }
    
    // 创建AI消息占位
    const aiMsgId = 'ai_' + Date.now();
    addMessageWithId('assistant', '', aiMsgId);
    
    try {
        // 使用AbortController设置超时
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60秒超时
        
        // 构建消息历史（最近10轮）
        const recentHistory = chatHistory.slice(-20); // 最近20条消息
        
        // 检测是否需要长回复（讲故事、写作等）
        const needLongReply = /故事|字|写作|作文|讲述|详细|完整/.test(msg);
        
        // 直连Ollama流式输出（带历史）
        const r = await fetch('/api/ollama/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                model: currentModel,
                messages: [
                    {role: 'system', content: getSystemPrompt()},
                    ...recentHistory
                ],
                stream: true,
                options: {
                    num_predict: needLongReply ? 4096 : 2048,  // 长回复用更多 token
                    temperature: 0.8
                }
            }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!r.ok) {
            throw new Error(`HTTP ${r.status}: ${r.statusText}`);
        }
        
        const reader = r.body.getReader();
        const decoder = new TextDecoder();
        let fullAnswer = '';
        
        while (true) {
            const {done, value} = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.trim()) {
                    try {
                        const d = JSON.parse(line);
                        if (d.message?.content) {
                            fullAnswer += d.message.content;
                            updateMessage(aiMsgId, fullAnswer);
                        }
                        // 检查错误
                        if (d.error) {
                            throw new Error(d.error);
                        }
                    } catch(e) {
                        if (e.message && !e.message.includes('JSON')) {
                            throw e;
                        }
                    }
                }
            }
        }
        
        if (!fullAnswer) {
            updateMessage(aiMsgId, '抱歉，没有获取到回复，请重试');
        } else {
            // 添加到历史
            chatHistory.push({role: 'assistant', content: fullAnswer});
        }
    } catch(e) {
        console.error('聊天错误:', e);
        let errorMsg = '❌ 网络错误';
        if (e.name === 'AbortError') {
            errorMsg = '⏱️ 请求超时，请重试';
        } else if (e.message) {
            errorMsg = '❌ ' + e.message;
        }
        updateMessage(aiMsgId, errorMsg);
    }
    
    isProcessing = false;
}

// 小熊老师提示词（模块化）
function getSystemPrompt() {
    const now = new Date();
    const timeStr = now.toLocaleString('zh-CN', {timeZone: 'Asia/Shanghai'});
    const hour = now.getHours();
    const lunarData = {'2026-05-10': '三月十四', '2026-05-11': '三月十五'};
    const lunar = lunarData[now.toISOString().slice(0, 10)] || '三月十四';
    
    return `你是"小熊老师🧸"，一个专业的家庭教育AI助手。

当前时间：${timeStr} 农历：${lunar}

【模块识别】根据关键词匹配唯一模块：
1.【美食智库】菜谱、食谱、辅食、做饭、烹饪、怎么吃
2.【K12学科辅导】做题、判题、纠错、年级、科目、算术、作文、公式、对吗、正确吗
3.【安全防护】急救、安全、地震、火灾、烫伤、防护
4.【孕产育儿】备孕、孕期、产后、宝宝、育儿、疫苗
5.【财商启蒙】零花钱、理财、压岁钱、存钱、预算
6.【睡前故事】讲故事、睡前故事、童话、寓言
7.【家校协同】家长会、老师、学校、教育政策

【回答规则】
- 先判断模块，以【模块名】开头
- K12判题必含：纠错→思路→步骤→方法→课本定位(冀教版)
- 简单问题一句话，闲聊/讲故事可详细
- ${hour >= 22 ? '晚上10点后，建议休息，不建议户外活动' : ''}
- 不匹配任何模块时说：我是家庭教育助手，这个问题不在我的能力范围

记住之前的对话，保持连贯。`;
}

function getLunarDate(date) {
    const lunarData = {'2026-05-10': '三月十四', '2026-05-11': '三月十五'};
    return lunarData[date.toISOString().slice(0, 10)] || '三月十四';
}

function getHolidaysInfo() { return ''; }

// 检查工具
function checkTools(msg) {
    const q = msg.toLowerCase();
    const cities = ['北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都', '重庆', '西安', '天津', '苏州', '青岛', '石家庄'];
    const weatherKeywords = ['天气', '温度', '气温'];
    
    const hasCity = cities.some(c => msg.includes(c));
    const hasWeather = weatherKeywords.some(k => q.includes(k));
    
    if (hasCity && hasWeather) {
        return {type: 'weather', city: cities.find(c => msg.includes(c)), isTomorrow: q.includes('明天')};
    }
    return null;
}

// 检查节日查询
function checkHolidayQuery(msg) {
    const q = msg.toLowerCase();
    
    // 2026年节日数据
    const holidays = {
        '春节': '2026年2月17日（农历正月初一）',
        '元宵节': '2026年3月3日（农历正月十五）',
        '清明节': '2026年4月5日',
        '劳动节': '2026年5月1日',
        '端午节': '2026年5月31日（农历五月初五）',
        '七夕节': '2026年8月19日（农历七月初七）',
        '中秋节': '2026年9月25日（农历八月十五）',
        '国庆节': '2026年10月1日',
        '重阳节': '2026年10月18日（农历九月初九）',
        '元旦': '2026年1月1日',
        '五一': '2026年5月1日',
        '十一': '2026年10月1日',
    };
    
    // 检查是否问节日
    for (const [name, date] of Object.entries(holidays)) {
        if (msg.includes(name) && (q.includes('几') || q.includes('哪') || q.includes('什么') || q.includes('什么时候') || q.includes('日期') || q.includes('时间'))) {
            return `${name}是${date}哦！🎉`;
        }
    }
    
    return null;
}

// 天气查询
async function getWeather(city, isTomorrow) {
    const cityMap = {
        '北京': 'Beijing', '上海': 'Shanghai', '广州': 'Guangzhou', '深圳': 'Shenzhen',
        '杭州': 'Hangzhou', '南京': 'Nanjing', '武汉': 'Wuhan', '成都': 'Chengdu',
        '重庆': 'Chongqing', '西安': 'Xian', '天津': 'Tianjin', '苏州': 'Suzhou',
        '青岛': 'Qingdao', '石家庄': 'Shijiazhuang'
    };
    
    try {
        const cityEn = cityMap[city] || 'Beijing';
        const r = await fetch(`http://wttr.in/${cityEn}?format=j1`);
        const data = await r.json();
        
        const weatherMap = {
            'Sunny': '晴', 'Clear': '晴', 'Partly cloudy': '多云', 'Cloudy': '阴',
            'Rain': '雨', 'Light rain': '小雨'
        };
        
        if (isTomorrow) {
            const tomorrow = data.weather[1] || {};
            const maxTemp = tomorrow.maxtempC || '?';
            const minTemp = tomorrow.mintempC || '?';
            const weatherDesc = tomorrow.hourly?.[0]?.weatherDesc?.[0]?.value || '未知';
            const weatherCn = weatherMap[weatherDesc] || weatherDesc;
            return `🌤️ ${city}明天天气：${weatherCn}\n\n🌡️ 温度：${minTemp}°C ~ ${maxTemp}°C`;
        } else {
            const current = data.current_condition[0];
            const today = data.weather[0];
            const weatherDesc = current.weatherDesc[0].value;
            const weatherCn = weatherMap[weatherDesc] || weatherDesc;
            return `🌤️ ${city}今天天气：${weatherCn}\n\n🌡️ 温度：${today.mintempC}°C ~ ${today.maxtempC}°C\n📍 当前：${current.temp_C}°C`;
        }
    } catch(e) {
        return null;
    }
}

// 添加带ID的消息
function addMessageWithId(role, content, id) {
    const container = document.getElementById('chatMessages');
    const time = new Date().toLocaleTimeString('zh-CN', {hour:'2-digit', minute:'2-digit'});
    
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.id = id;
    div.innerHTML = `
        <div class="msg-avatar">${role === 'user' ? '👤' : '🧸'}</div>
        <div class="msg-content">
            <div class="msg-bubble">${escapeHtml(content) || '<div class="thinking">⏳ 正在思考...</div>'}</div>
            <div class="msg-time">${time}</div>
        </div>
    `;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// 更新消息内容
function updateMessage(id, content) {
    const el = document.getElementById(id);
    if (el) {
        const bubble = el.querySelector('.msg-bubble');
        if (bubble) {
            bubble.innerHTML = escapeHtml(content);
            el.querySelector('.msg-time').textContent = new Date().toLocaleTimeString('zh-CN', {hour:'2-digit', minute:'2-digit'});
        }
    }
    const container = document.getElementById('chatMessages');
    container.scrollTop = container.scrollHeight;
}

// 添加消息
function addMessage(role, content) {
    const container = document.getElementById('chatMessages');
    const time = new Date().toLocaleTimeString('zh-CN', {hour:'2-digit', minute:'2-digit'});
    
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerHTML = `
        <div class="msg-avatar">${role === 'user' ? '👤' : '🧸'}</div>
        <div class="msg-content">
            <div class="msg-bubble">${escapeHtml(content)}</div>
            <div class="msg-time">${time}</div>
        </div>
    `;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 键盘事件
function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

// 语音识别
let isRecording = false;
function toggleVoice() {
    const btn = document.getElementById('voiceBtn');
    
    if (!isRecording) {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('您的浏览器不支持语音识别');
            return;
        }
        
        try {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'zh-CN';
            
            recognition.onstart = () => {
                isRecording = true;
                btn.classList.add('recording');
                btn.innerHTML = '⏹️';
            };
            
            recognition.onresult = (e) => {
                document.getElementById('chatInput').value = e.results[0][0].transcript;
                sendMessage();
            };
            
            recognition.onerror = (e) => {
                alert('语音识别失败：' + e.error);
                isRecording = false;
                btn.classList.remove('recording');
                btn.innerHTML = '🎤';
            };
            
            recognition.onend = () => {
                isRecording = false;
                btn.classList.remove('recording');
                btn.innerHTML = '🎤';
            };
            
            recognition.start();
        } catch(e) {
            alert('语音识别启动失败');
        }
    }
}

// 已选择的题型
let selectedExamTypes = [];

// 添加题型标签
function addTypeTag() {
    const select = document.getElementById('examTypeSelect');
    const value = select.value;
    if (!value) return;
    
    // 避免重复添加
    if (selectedExamTypes.includes(value)) {
        select.value = '';
        return;
    }
    
    selectedExamTypes.push(value);
    renderTypeTags();
    select.value = '';
}

// 渲染题型标签
function renderTypeTags() {
    const container = document.getElementById('typeTags');
    const typeNames = {
        '分解组成': '分解与组成',
        '口算题': '口算题',
        '计算题': '计算题',
        '填空题': '填空题',
        '判断题': '判断题',
        '选择题': '选择题',
        '应用题': '应用题',
        '比大小': '比大小'
    };
    
    container.innerHTML = selectedExamTypes.map(type => `
        <span style="display:inline-flex;align-items:center;gap:4px;padding:4px 10px;background:var(--primary);color:white;border-radius:16px;font-size:13px">
            ${typeNames[type] || type}
            <span onclick="removeTypeTag('${type}')" style="cursor:pointer;margin-left:2px">✕</span>
        </span>
    `).join('');
}

// 移除题型标签
function removeTypeTag(type) {
    selectedExamTypes = selectedExamTypes.filter(t => t !== type);
    renderTypeTags();
}

// 获取选中的题型
function getSelectedTypes() {
    return selectedExamTypes;
}

// 生成试卷
async function generateExam() {
    const grade = document.getElementById('examGrade').value;
    const subject = document.getElementById('examSubject').value;
    const selectedTypes = getSelectedTypes();
    const count = parseInt(document.getElementById('examCount').value);
    
    const result = document.getElementById('examResult');
    const content = document.getElementById('examContent');
    result.style.display = 'block';
    content.innerHTML = '<div class="thinking">⏳ 正在生成试卷...</div>';
    
    try {
        const r = await fetch('/api/exam/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({grade, subject, exam_types: selectedTypes, count, child_id: currentChild})
        });
        const d = await r.json();
        
        if (d.success && d.questions) {
            // 保存题目用于打印
            currentQuestions = d.questions;
            
            // 按题型分组显示
            const typeOrder = ['分解与组成', '填空题', '选择题', '判断题', '应用题', '比大小', '口算题', '综合题'];
            const typeGroups = {};
            d.questions.forEach((q, i) => {
                const type = q.type || '综合题';
                if (!typeGroups[type]) typeGroups[type] = [];
                typeGroups[type].push({...q, originalIndex: i});
            });
            
            // 题目部分（按题型分组显示）
            let html = '<div style="margin-bottom:24px">';
            let questionNum = 1;
            
            typeOrder.forEach(type => {
                if (!typeGroups[type] || typeGroups[type].length === 0) return;
                
                html += `<div style="margin-bottom:24px">
                    <h4 style="margin-bottom:12px;color:var(--primary);padding:8px 12px;background:linear-gradient(90deg,#f0f9ff,#e0f2fe);border-radius:6px">${getTypeIcon(type)} ${type}</h4>`;
                
                typeGroups[type].forEach(q => {
                    // 图形化题目（分解与组成）用 pre 标签
                    let questionText;
                    if (q.is_graphic || type === '分解与组成') {
                        questionText = `<pre style="font-family:monospace;font-size:18px;line-height:1.2;margin:8px 0;white-space:pre;background:transparent">${q.question}</pre>`;
                    } else {
                        questionText = formatQuestion(q.question);
                    }
                    
                    html += `
                    <div style="margin-bottom:12px;padding:12px;background:var(--bg-main);border-radius:8px">
                        <div><b>${questionNum}.</b> ${questionText}</div>
                    </div>`;
                    questionNum++;
                });
                
                html += '</div>';
            });
            
            html += '</div>';
            
            // 答案部分（按题型分组显示）
            html += '<div style="margin-top:32px;padding-top:16px;border-top:2px dashed var(--border)"><h3 style="margin-bottom:16px;color:var(--primary)">📋 答案</h3>';
            
            questionNum = 1;
            typeOrder.forEach(type => {
                if (!typeGroups[type] || typeGroups[type].length === 0) return;
                
                html += `<div style="margin-bottom:16px">
                    <div style="font-size:12px;color:var(--text-secondary);margin-bottom:8px">${type}</div>
                    <div style="display:flex;flex-wrap:wrap;gap:8px">`;
                
                typeGroups[type].forEach(q => {
                    const answer = q.answer || '略';
                    // 选择题答案换行显示
                    if (type === '选择题') {
                        html += `<div style="padding:8px 12px;background:#f0fdf4;border-radius:6px;border:1px solid var(--border);min-width:80px;text-align:center">
                            <b>${questionNum}.</b><br><span style="color:var(--primary);font-weight:600">${answer}</span>
                        </div>`;
                    } else {
                        html += `<div style="padding:6px 12px;background:#f0fdf4;border-radius:6px;border:1px solid var(--border);min-width:60px;text-align:center">
                            <b>${questionNum}.</b> ${answer}
                        </div>`;
                    }
                    questionNum++;
                });
                
                html += '</div></div>';
            });
            
            // 解析部分（如果有）
            const hasExplanation = d.questions.some(q => q.explanation);
            if (hasExplanation) {
                html += '<div style="margin-top:20px"><h4 style="margin-bottom:12px;color:var(--text-secondary)">📝 解析</h4>';
                d.questions.forEach((q, i) => {
                    if (q.explanation) {
                        html += `<div style="margin-bottom:8px;padding:8px 12px;background:var(--bg-main);border-radius:6px;border-left:3px solid var(--primary)">
                            <b>${i+1}.</b> ${q.explanation}
                        </div>`;
                    }
                });
                html += '</div>';
            }
            html += '</div>';
            
            // 添加打印按钮
            html += '<div style="margin-top:16px;text-align:center"><button class="btn btn-primary" onclick="printExam()">🖨️ 打印试卷</button></div>';
            
            content.innerHTML = html;
        } else {
            content.innerHTML = '<div style="color:#ef4444">' + (d.error || '生成失败') + '</div>';
        }
    } catch(e) {
        content.innerHTML = '<div style="color:#ef4444">生成失败：' + e.message + '</div>';
    }
}

// 获取题型图标
function getTypeIcon(type) {
    const icons = {
        '分解与组成': '🔢',
        '填空题': '✏️',
        '选择题': '🔘',
        '判断题': '⚖️',
        '应用题': '📖',
        '比大小': '📐',
        '口算题': '🧮',
        '综合题': '📝'
    };
    return icons[type] || '📝';
}

// 格式化题目（把 ? 和 ___ 替换成括号）
function formatQuestion(text) {
    if (!text) return '';
    // 替换 ? 和 ？ 为括号
    text = text.replace(/\?/g, '（  ）');
    text = text.replace(/？/g, '（  ）');
    // 替换 ___ 为括号
    text = text.replace(/_+/g, '（  ）');
    return text;
}

// 打印试卷（题目和答案分页）
function printExam() {
    if (!currentQuestions || currentQuestions.length === 0) {
        alert('请先生成试卷');
        return;
    }
    
    const win = window.open('', '_blank', 'width=800,height=600');
    win.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>练习题</title>
            <style>
                body { font-family: 'Microsoft YaHei', sans-serif; padding: 40px; line-height: 2; font-size: 16px; }
                .header { text-align: center; margin-bottom: 30px; font-size: 14px; color: #666; border-bottom: 2px solid #333; padding-bottom: 15px; }
                h2 { text-align: center; margin-bottom: 30px; }
                .question { margin-bottom: 25px; page-break-inside: avoid; }
                .question-num { font-weight: bold; margin-right: 8px; }
                .page-break { page-break-after: always; }
                .answers { display: flex; flex-wrap: wrap; gap: 12px; }
                .answer-item { padding: 6px 16px; background: #f0f0f0; border-radius: 4px; min-width: 80px; text-align: center; }
                pre { font-family: monospace; font-size: 18px; line-height: 1.4; margin: 8px 0; }
            </style>
        </head>
        <body>
            <div class="header">姓名：__________ 日期：__________ 得分：__________</div>
            <h2>📝 练习题</h2>
            ${currentQuestions.map((q, i) => {
                const qText = q.is_graphic ? `<pre>${q.question}</pre>` : formatQuestion(q.question);
                return `<div class="question">
                    <span class="question-num">${i+1}.</span>${qText}
                </div>`;
            }).join('')}
            
            <div class="page-break"></div>
            
            <!-- 第二页：答案 -->
            <h2>📋 答案</h2>
            <div class="answers">
                ${currentQuestions.map((q, i) => `<div class="answer-item"><b>${i+1}.</b> ${q.answer || '略'}</div>`).join('')}
            </div>
            
            ${currentQuestions.some(q => q.explanation) ? `
            <div style="margin-top:30px">
                <h3>📝 解析</h3>
                ${currentQuestions.map((q, i) => q.explanation ? 
                    `<div style="margin:12px 0;padding:10px;background:#f9f9f9;border-left:3px solid #6366f1">
                        <b>${i+1}.</b> ${q.explanation}
                    </div>` : ''
                ).join('')}
            </div>
            ` : ''}
        </body>
        </html>
    `);
    win.document.close();
    win.print();
}

// 处理照片
async function handlePhoto(input) {
    if (!input.files[0]) return;
    
    const result = document.getElementById('photoResult');
    const content = document.getElementById('photoContent');
    result.style.display = 'block';
    content.innerHTML = '<div class="thinking">⏳ 正在压缩图片...</div>';
    
    try {
        // 压缩图片
        const compressedFile = await compressImage(input.files[0]);
        console.log(`图片压缩：${(input.files[0].size / 1024).toFixed(1)}KB → ${(compressedFile.size / 1024).toFixed(1)}KB`);
        
        content.innerHTML = '<div class="thinking">⏳ 正在识别和批改（可能需要1-2分钟）...</div>';
        
        const formData = new FormData();
        formData.append('photo', compressedFile);
        formData.append('child_id', currentChild);
        
        // 增加超时时间到 3 分钟
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 180000);
        
        const r = await fetch('/api/photo', {
            method: 'POST', 
            body: formData,
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!r.ok) {
            throw new Error(`服务器错误：${r.status}`);
        }
        
        const d = await r.json();
        
        if (d.success && d.result) {
            content.innerHTML = `
                <div style="margin-bottom:16px">
                    <h4 style="margin-bottom:8px">📝 识别结果</h4>
                    <pre style="white-space:pre-wrap;background:var(--bg-main);padding:12px;border-radius:8px">${d.result}</pre>
                </div>
                <div style="text-align:center;margin-top:16px">
                    <button class="btn btn-primary" onclick="gradePhoto('${encodeURIComponent(d.result)}')">✏️ 开始批改</button>
                </div>
            `;
        } else {
            content.innerHTML = `<div style="color:#ef4444">${d.error || '识别失败'}</div>`;
        }
    } catch(e) {
        if (e.name === 'AbortError') {
            content.innerHTML = '<div style="color:#ef4444">⏱️ 请求超时，请重试或使用更小的图片</div>';
        } else {
            content.innerHTML = '<div style="color:#ef4444">识别失败：' + e.message + '</div>';
        }
    }
}

// 压缩图片
async function compressImage(file) {
    return new Promise((resolve, reject) => {
        // 如果小于 500KB，直接返回
        if (file.size < 500 * 1024) {
            resolve(file);
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                
                // 计算压缩后的尺寸（最大 1920px）
                let width = img.width;
                let height = img.height;
                const maxSize = 1920;
                
                if (width > maxSize || height > maxSize) {
                    if (width > height) {
                        height = (height / width) * maxSize;
                        width = maxSize;
                    } else {
                        width = (width / height) * maxSize;
                        height = maxSize;
                    }
                }
                
                canvas.width = width;
                canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);
                
                // 压缩质量 0.7
                canvas.toBlob((blob) => {
                    if (blob) {
                        const compressedFile = new File([blob], file.name, { type: 'image/jpeg' });
                        resolve(compressedFile);
                    } else {
                        reject(new Error('压缩失败'));
                    }
                }, 'image/jpeg', 0.7);
            };
            img.onerror = () => reject(new Error('图片加载失败'));
            img.src = e.target.result;
        };
        reader.onerror = () => reject(new Error('文件读取失败'));
        reader.readAsDataURL(file);
    });
}

// 批改作业
async function gradePhoto(extractedText) {
    const text = decodeURIComponent(extractedText);
    const content = document.getElementById('photoContent');
    content.innerHTML = '<div class="thinking">⏳ 正在批改...</div>';
    
    try {
        const r = await fetch('/api/photo/grade', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({extracted: text, child_id: currentChild})
        });
        
        const d = await r.json();
        
        if (d.success && d.grade) {
            const g = d.grade;
            content.innerHTML = `
                <div style="margin-bottom:16px">
                    <div style="display:flex;gap:16px;margin-bottom:16px">
                        <div style="flex:1;padding:16px;background:var(--bg-main);border-radius:8px;text-align:center">
                            <div style="font-size:24px;font-weight:bold;color:var(--primary)">${g.correct || 0}/${g.total || 0}</div>
                            <div style="color:var(--text-secondary);font-size:12px">正确/总数</div>
                        </div>
                    </div>
                    ${g.wrong_questions && g.wrong_questions.length > 0 ? `
                    <div style="margin-top:16px">
                        <h4 style="margin-bottom:8px">❌ 错题分析</h4>
                        ${g.wrong_questions.map((wq, i) => `
                            <div style="margin-bottom:12px;padding:12px;background:#fef2f2;border-radius:8px;border-left:3px solid #ef4444">
                                <div style="font-weight:600">${i+1}. ${wq.question || ''}</div>
                                <div style="margin-top:4px;color:#ef4444">你的答案：${wq.student_answer || ''}</div>
                                <div style="color:#10b981">正确答案：${wq.correct_answer || ''}</div>
                            </div>
                        `).join('')}
                    </div>
                    ` : '<div style="text-align:center;padding:20px;color:#10b981">🎉 全部正确！</div>'}
                    ${g.diagnosis ? `
                    <div style="margin-top:16px;padding:12px;background:#f0fdf4;border-radius:8px">
                        <h4 style="margin-bottom:8px">📊 诊断建议</h4>
                        <div>${g.diagnosis}</div>
                    </div>
                    ` : ''}
                </div>
            `;
        } else {
            content.innerHTML = `<div style="color:#ef4444">${d.error || '批改失败'}</div>`;
        }
    } catch(e) {
        content.innerHTML = '<div style="color:#ef4444">批改失败：' + e.message + '</div>';
    }
}

// 生成学习计划
async function generatePlan() {
    const grade = document.getElementById('planGrade').value;
    const subject = document.getElementById('planSubject').value;
    
    const result = document.getElementById('planResult');
    const content = document.getElementById('planContent');
    result.style.display = 'block';
    content.innerHTML = '<div class="thinking">⏳ 正在生成学习计划...</div>';
    
    try {
        const r = await fetch('/api/plan/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({grade, subject, child_id: currentChild})
        });
        const d = await r.json();
        
        if (d.success && d.plan) {
            content.innerHTML = `
                <div class="card-title">本周学习目标</div>
                <p>${d.plan.goal || ''}</p>
                <div class="card-title" style="margin-top:16px">每日安排</div>
                ${(d.plan.daily || []).map(d => `<div style="padding:8px 0;border-bottom:1px solid var(--border)">• ${d}</div>`).join('')}
            `;
        }
    } catch(e) {
        content.innerHTML = '<div style="color:#ef4444">生成失败</div>';
    }
}

// 加载知识库
async function loadKnowledge() {
    try {
        const r = await fetch('/api/kb/list?child_id=' + currentChild);
        const d = await r.json();
        const list = document.getElementById('knowledgeList');
        
        if (d.files && d.files.length > 0) {
            list.innerHTML = d.files.map(f => `
                <div style="padding:12px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center">
                    <span>📄 ${f.filename}</span>
                    <span style="color:var(--text-secondary)">${f.text_len}字</span>
                </div>
            `).join('');
        } else {
            list.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-secondary)">暂无资料</div>';
        }
    } catch(e) {
        document.getElementById('knowledgeList').innerHTML = '<div style="color:#ef4444">加载失败</div>';
    }
}

// 上传知识库
async function uploadKnowledge(input) {
    if (!input.files[0]) return;
    
    const formData = new FormData();
    formData.append('file', input.files[0]);
    formData.append('child_id', currentChild);
    
    try {
        const r = await fetch('/upload', {method: 'POST', body: formData});
        const d = await r.json();
        alert(d.message || '上传成功');
        loadKnowledge();
    } catch(e) {
        alert('上传失败');
    }
}

// 快捷操作菜单
function showQuickActions() {
    const menu = document.getElementById('quickActions');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

function insertTemplate(type) {
    const input = document.getElementById('chatInput');
    const templates = {
        '出题': '请帮我出10道一年级的数学题，包括口算题、填空题和应用题',
        '判题': '我要拍照上传作业，请帮我批改',
        '讲解': '请给我讲解一下这个知识点：',
        '计划': '请帮我制定一个学习计划'
    };
    input.value = templates[type] || '';
    input.focus();
    document.getElementById('quickActions').style.display = 'none';
}

// 点击其他地方关闭菜单
document.addEventListener('click', function(e) {
    const menu = document.getElementById('quickActions');
    if (menu && !e.target.closest('#quickActions') && !e.target.closest('.action-btn')) {
        menu.style.display = 'none';
    }
});

// 启动
init();
