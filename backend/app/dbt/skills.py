"""
DBT技能知识库
包含四大模块的标准化技能描述、指导步骤、适用场景
"""

from typing import Dict, List, Optional


# DBT技能数据库
SKILLS_DATABASE = {
    # 痛苦耐受技能 (Distress Tolerance)
    "TIPP": {
        "name": "TIPP",
        "category": "distress_tolerance",
        "introduction": "TIPP技能通过改变体温、剧烈运动、调整呼吸和放松肌肉来快速降低情绪强度",
        "适用场景": ["高强度焦虑", "愤怒失控", "恐慌发作"],
        "steps": [
            {
                "step": 1,
                "title": "Temperature（温度刺激）",
                "description": "用冷水洗脸或握住冰块30秒，刺激潜水反射，快速降低心率",
                "guidance": "找到冷水或冰块，将脸浸入冷水或用冰块敷在额头和脸颊上。如果没有冰块，可以用冷水洗脸。",
            },
            {
                "step": 2,
                "title": "Intense Exercise（剧烈运动）",
                "description": "进行5-10分钟的剧烈运动，如快跑、跳绳、开合跳等",
                "guidance": "选择你方便做的运动，比如原地跑步、做俯卧撑或深蹲。让你的心跳加速，直到感觉累了。",
            },
            {
                "step": 3,
                "title": "Paced Breathing（节律呼吸）",
                "description": "深呼吸，吸气5秒，呼气7秒，重复5分钟",
                "guidance": "慢慢地深吸一口气，数到5。然后缓慢呼气，数到7。重复这个过程，专注于你的呼吸。",
            },
            {
                "step": 4,
                "title": "Paired Muscle Relaxation（渐进式肌肉放松）",
                "description": "配合呼吸，逐步放松全身肌肉",
                "guidance": "吸气时绷紧肌肉，呼气时放松。从脚开始，逐渐向上到头部。",
            },
        ],
        "注意事项": "如果有心脏病或其他健康问题，请谨慎使用温度刺激和剧烈运动",
        "预期效果": "快速降低情绪强度2-4分",
    },
    "STOP": {
        "name": "STOP",
        "category": "distress_tolerance",
        "introduction": "STOP技能帮助你在冲动行为前暂停，避免做出后悔的决定",
        "适用场景": ["愤怒失控前", "想要冲动行动", "情绪高涨时"],
        "steps": [
            {
                "step": 1,
                "title": "Stop（停下来）",
                "description": "立即停止当前的行为或想法",
                "guidance": "不要动，不要说话，不要做任何事情。就像按下暂停键一样。",
            },
            {
                "step": 2,
                "title": "Take a step back（后退一步）",
                "description": "从情境中抽离，给自己空间",
                "guidance": "可以物理上后退一步，或者在心理上与情境拉开距离。深呼吸几次。",
            },
            {
                "step": 3,
                "title": "Observe（观察）",
                "description": "注意正在发生什么，观察你的想法和感受",
                "guidance": "问自己：'发生了什么？' '我有什么感受？' '我在想什么？'",
            },
            {
                "step": 4,
                "title": "Proceed mindfully（正念前行）",
                "description": "考虑你的目标和价值观，选择有效的行动",
                "guidance": "问自己：'什么行动最符合我的长期目标？' '怎样做对我最有利？'",
            },
        ],
        "注意事项": "这个技能需要练习才能在关键时刻使用",
        "预期效果": "避免冲动行为，帮助理性决策",
    },
    # 正念技能 (Mindfulness)
    "正念呼吸": {
        "name": "正念呼吸",
        "category": "mindfulness",
        "introduction": "通过专注于呼吸来稳定情绪，回到当下",
        "适用场景": ["轻度焦虑", "注意力涣散", "需要冷静时"],
        "steps": [
            {
                "step": 1,
                "title": "找到舒适的姿势",
                "description": "坐着或躺着都可以，让自己感觉舒适",
                "guidance": "闭上眼睛或保持眼睛半闭，找到一个让你感觉放松的姿势。",
            },
            {
                "step": 2,
                "title": "关注呼吸",
                "description": "将注意力集中在呼吸上，感受气息的进出",
                "guidance": "注意空气进入鼻腔的感觉，腹部的起伏，或者胸部的扩张和收缩。",
            },
            {
                "step": 3,
                "title": "当思绪飘走时",
                "description": "温和地把注意力带回到呼吸上",
                "guidance": "思绪游走是正常的。发现后，不要责怪自己，只需要温柔地把注意力带回呼吸。",
            },
            {
                "step": 4,
                "title": "持续5-10分钟",
                "description": "保持这个练习5-10分钟",
                "guidance": "如果时间充裕，可以练习更久。即使只有1-2分钟也有帮助。",
            },
        ],
        "注意事项": "不要强迫自己清空思绪，接纳任何出现的想法",
        "预期效果": "降低焦虑，提升专注力",
    },
    "一心一意": {
        "name": "一心一意",
        "category": "mindfulness",
        "introduction": "全神贯注地做一件事，不做其他事情",
        "适用场景": ["注意力分散", "多任务压力", "需要集中精力"],
        "steps": [
            {
                "step": 1,
                "title": "选择一项活动",
                "description": "选择一个简单的活动，如喝茶、走路或洗碗",
                "guidance": "选择一个你现在可以做的活动，不需要复杂。",
            },
            {
                "step": 2,
                "title": "专注于当前",
                "description": "把全部注意力放在这个活动上",
                "guidance": "感受每一个细节：温度、质地、声音、气味。",
            },
            {
                "step": 3,
                "title": "只做这一件事",
                "description": "不要同时做其他事情，不要边做边想别的",
                "guidance": "当你发现自己在想其他事情时，温柔地把注意力带回当前活动。",
            },
        ],
        "注意事项": "这不是要求你永远只做一件事，而是练习专注的能力",
        "预期效果": "提升专注力，减少焦虑",
    },
    "情绪命名": {
        "name": "情绪命名",
        "category": "mindfulness",
        "introduction": "准确识别和命名自己的情绪",
        "适用场景": ["情绪混乱", "不知道自己怎么了", "情绪涌现时"],
        "steps": [
            {
                "step": 1,
                "title": "停下来观察",
                "description": "暂停当前活动，关注内心",
                "guidance": "深呼吸几次，问自己：'我现在感觉如何？'",
            },
            {
                "step": 2,
                "title": "识别情绪",
                "description": "尝试给情绪命名：焦虑、悲伤、愤怒等",
                "guidance": "可能不止一种情绪。试着识别主要的情绪和次要的情绪。",
            },
            {
                "step": 3,
                "title": "接纳情绪",
                "description": "承认这个情绪是真实的，不评判它",
                "guidance": "对自己说：'我现在感到[情绪名称]，这是可以理解的。'",
            },
        ],
        "注意事项": "命名情绪不是为了消除它，而是为了理解它",
        "预期效果": "降低情绪强度，提升自我觉察",
    },
    # 情绪调节技能 (Emotion Regulation)
    "驾驭情绪之波": {
        "name": "驾驭情绪之波",
        "category": "emotion_regulation",
        "introduction": "像冲浪一样驾驭情绪的起伏，不被情绪淹没",
        "适用场景": ["强烈悲伤", "情绪波动", "感觉被情绪淹没"],
        "steps": [
            {
                "step": 1,
                "title": "承认情绪波浪",
                "description": "认识到情绪像波浪一样会起伏",
                "guidance": "告诉自己：'这个情绪会像波浪一样，升起、达到高峰、然后消退。'",
            },
            {
                "step": 2,
                "title": "不要抵抗",
                "description": "不要试图压制或逃避情绪",
                "guidance": "想象自己是一个冲浪者，顺着波浪的方向前进，而不是对抗它。",
            },
            {
                "step": 3,
                "title": "观察波浪",
                "description": "观察情绪如何升起、达到高峰、然后消退",
                "guidance": "注意情绪的变化，但不被它控制。记住，波浪总会过去。",
            },
        ],
        "注意事项": "这需要练习，一开始可能很难做到",
        "预期效果": "减少对情绪的恐惧，提升情绪耐受力",
    },
    "自我安抚": {
        "name": "自我安抚",
        "category": "emotion_regulation",
        "introduction": "通过五感（视觉、听觉、嗅觉、味觉、触觉）来安抚自己",
        "适用场景": ["需要安慰", "情绪低落", "感到孤独"],
        "steps": [
            {
                "step": 1,
                "title": "视觉安抚",
                "description": "看一些美好的事物",
                "guidance": "可以是美丽的风景照片、艺术作品，或者窗外的风景。",
            },
            {
                "step": 2,
                "title": "听觉安抚",
                "description": "听一些舒缓的音乐或自然声音",
                "guidance": "选择让你感觉放松的音乐，或者听雨声、海浪声等。",
            },
            {
                "step": 3,
                "title": "嗅觉安抚",
                "description": "闻一些喜欢的气味",
                "guidance": "可以是香水、精油、咖啡、鲜花等。",
            },
            {
                "step": 4,
                "title": "味觉安抚",
                "description": "品尝一些喜欢的食物",
                "guidance": "慢慢品尝，专注于食物的味道和口感。",
            },
            {
                "step": 5,
                "title": "触觉安抚",
                "description": "触摸柔软或温暖的东西",
                "guidance": "可以是毛毯、宠物、热水袋等。",
            },
        ],
        "注意事项": "选择健康的安抚方式，避免过度依赖某种方式",
        "预期效果": "提升舒适感，降低情绪强度",
    },
    "积极体验": {
        "name": "积极体验",
        "category": "emotion_regulation",
        "introduction": "主动创造积极的情绪体验",
        "适用场景": ["情绪低落", "缺乏动力", "需要提升情绪"],
        "steps": [
            {
                "step": 1,
                "title": "列出愉快活动",
                "description": "想一想有哪些活动会让你感觉好一些",
                "guidance": "可以是简单的活动：听音乐、看电影、散步、和朋友聊天等。",
            },
            {
                "step": 2,
                "title": "选择一项活动",
                "description": "从列表中选择一项你现在可以做的",
                "guidance": "不要选择太复杂的活动，从简单的开始。",
            },
            {
                "step": 3,
                "title": "全身心投入",
                "description": "专注地去体验这个活动",
                "guidance": "尽可能地沉浸在活动中，享受当下的感觉。",
            },
        ],
        "注意事项": "即使开始时不太想做，也可以尝试，通常做了之后会感觉好一些",
        "预期效果": "提升情绪，增加正向体验",
    },
    # 人际效能技能 (Interpersonal Effectiveness)
    "求助朋友": {
        "name": "求助朋友",
        "category": "interpersonal",
        "introduction": "有效地向他人寻求帮助和支持",
        "适用场景": ["需要支持", "感到孤独", "遇到困难"],
        "steps": [
            {
                "step": 1,
                "title": "识别支持对象",
                "description": "想一想谁是你可以信任的人",
                "guidance": "可以是朋友、家人、老师或咨询师。选择一个你感觉安全的人。",
            },
            {
                "step": 2,
                "title": "明确你的需求",
                "description": "想清楚你需要什么帮助",
                "guidance": "是需要倾听？建议？陪伴？还是实际的帮助？",
            },
            {
                "step": 3,
                "title": "表达你的需求",
                "description": "清楚地告诉对方你需要什么",
                "guidance": "可以说：'我现在感觉很难过，需要有人听我说说话。' 或 '我需要一些建议。'",
            },
        ],
        "注意事项": "寻求帮助是勇敢的表现，不是软弱",
        "预期效果": "获得支持，减少孤独感",
    },
    # 其他常用技能
    "感恩练习": {
        "name": "感恩练习",
        "category": "mindfulness",
        "introduction": "关注生活中值得感恩的事物",
        "适用场景": ["情绪低落", "负面思维", "需要积极视角"],
        "steps": [
            {
                "step": 1,
                "title": "回顾今天",
                "description": "想一想今天发生的事情",
                "guidance": "不需要是很重大的事情，小事也可以。",
            },
            {
                "step": 2,
                "title": "列出三件感恩的事",
                "description": "找出三件值得感恩的事情",
                "guidance": "可以写下来：'今天天气很好'、'朋友发了关心的消息'、'午餐很美味'等。",
            },
            {
                "step": 3,
                "title": "体会感恩的感觉",
                "description": "花点时间真正感受感恩",
                "guidance": "不只是列出来，而是真正去体会这些事情带来的好感觉。",
            },
        ],
        "注意事项": "这不是要否认困难，而是平衡视角",
        "预期效果": "提升情绪，培养积极心态",
    },
    "接地技术": {
        "name": "接地技术",
        "category": "distress_tolerance",
        "introduction": "通过感官体验把注意力带回当下",
        "适用场景": ["焦虑发作", "思维混乱", "感觉失控"],
        "steps": [
            {
                "step": 1,
                "title": "5-4-3-2-1技术",
                "description": "用五感体验当下",
                "guidance": "找出5样你能看到的东西，4样你能触摸的，3样你能听到的，2样你能闻到的，1样你能尝到的。",
            },
            {
                "step": 2,
                "title": "脚踏实地",
                "description": "感受双脚与地面的接触",
                "guidance": "站立或坐着，注意双脚踩在地上的感觉。用力压地面，感受稳定感。",
            },
        ],
        "注意事项": "这个技能可以随时随地使用",
        "预期效果": "快速回到当下，减少焦虑"
    },

    # 人际效能技能补充
    "DEAR MAN": {
        "name": "DEAR MAN",
        "category": "interpersonal",
        "introduction": "有效地向他人表达需求和拒绝不合理要求的技能",
        "适用场景": ["需要表达观点", "被强迫同意", "需要维护权益"],
        "steps": [
            {
                "step": 1,
                "title": "Describe（描述）",
                "description": "客观地描述情况，不加感情色彩",
                "guidance": "清晰地说出事实。例如：'你答应周末陪我，但现在说要取消。'"
            },
            {
                "step": 2,
                "title": "Express（表达）",
                "description": "表达你的想法和感受",
                "guidance": "用'我'开头：'我对这个决定感到失望。'"
            },
            {
                "step": 3,
                "title": "Assert（坚持）",
                "description": "坚定地提出你的要求",
                "guidance": "明确说出你需要什么：'我需要你按约定陪我。'"
            },
            {
                "step": 4,
                "title": "Reinforce（强化）",
                "description": "解释你的要求为什么重要，说明好处",
                "guidance": "'这对我很重要，我们一起度过时光能增进感情。'"
            }
        ],
        "注意事项": "保持冷静和尊重，即使对方拒绝也是可以接受的",
        "预期效果": "有效表达需求，改善沟通"
    },

    "GIVE": {
        "name": "GIVE",
        "category": "interpersonal",
        "introduction": "维护和改善人际关系的技能",
        "适用场景": ["关系冲突", "想要改善关系", "人际危机"],
        "steps": [
            {
                "step": 1,
                "title": "Gentle（温柔）",
                "description": "用温柔的态度和语气对待他人",
                "guidance": "避免批评、抱怨或讽刺。使用平和的语气和友善的表情。"
            },
            {
                "step": 2,
                "title": "Interested（感兴趣）",
                "description": "表现出对他人的真实兴趣",
                "guidance": "问问他们的情况，认真倾听。记住他们说的话，表现出关心。"
            },
            {
                "step": 3,
                "title": "Validate（认可）",
                "description": "确认他人的感受是有道理的",
                "guidance": "说出像'我理解你为什么生气'或'你的感受是合理的'这样的话。"
            },
            {
                "step": 4,
                "title": "Easy manner（轻松自在）",
                "description": "使用幽默和轻松的方式",
                "guidance": "适当使用幽默，笑脸相迎，让气氛变得轻松。"
            }
        ],
        "注意事项": "真诚是最重要的，不能假装关心",
        "预期效果": "改善关系，增进理解"
    },

    "FAST": {
        "name": "FAST",
        "category": "interpersonal",
        "introduction": "在沟通中保持自尊和诚实的技能",
        "适用场景": ["需要拒绝", "被操纵时", "需要坚持原则"],
        "steps": [
            {
                "step": 1,
                "title": "Fair（公平）",
                "description": "对自己和他人都公平对待",
                "guidance": "既要考虑自己的需要，也要考虑对方的需要。不要过度退让或过度坚持。"
            },
            {
                "step": 2,
                "title": "Apologies（道歉）",
                "description": "只为你真正做错的事道歉",
                "guidance": "不要为了平复冲突就无谓地道歉。'我遗憾地'可以代替'我很抱歉'。"
            },
            {
                "step": 3,
                "title": "Stick to values（坚持价值观）",
                "description": "坚守你的价值观和原则",
                "guidance": "不要为了讨好别人而违反你的原则。问问自己：'这与我的价值观一致吗？'"
            },
            {
                "step": 4,
                "title": "Truthful（诚实）",
                "description": "保持诚实，不要说谎",
                "guidance": "即使说实话会带来不适，也要坚持真实。诚实比一时的和平更重要。"
            }
        ],
        "注意事项": "自尊并不意味着自私，而是自我尊重",
        "预期效果": "保持自尊，建立诚实的关系"
    },

    "设定边界": {
        "name": "设定边界",
        "category": "interpersonal",
        "introduction": "在人际关系中清晰地表达自己的限制和需要",
        "适用场景": ["受到不尊重", "被过度依赖", "关系中感到疲惫"],
        "steps": [
            {
                "step": 1,
                "title": "识别你的界限",
                "description": "明确你能接受什么，不能接受什么",
                "guidance": "写下来：'我不能容忍的是...' '我需要的是...'"
            },
            {
                "step": 2,
                "title": "清楚地表达",
                "description": "用明确的语言表达你的界限",
                "guidance": "'我不能每天接听你的电话。我们可以定在周末谈话。'"
            },
            {
                "step": 3,
                "title": "保持一致",
                "description": "每次都坚持你的界限",
                "guidance": "即使对方生气或失望，也要坚持你的界限。一致性才能让界限有效。"
            },
            {
                "step": 4,
                "title": "接受后果",
                "description": "准备好接受设定界限可能带来的后果",
                "guidance": "对方可能会感到不满或远离，这是可以接受的。"
            }
        ],
        "注意事项": "设定边界不是自私，而是自我保护和尊重",
        "预期效果": "改善关系质量，减少被利用感"
    },

    # 痛苦耐受技能补充
    "ACCEPTS": {
        "name": "ACCEPTS",
        "category": "distress_tolerance",
        "introduction": "通过分散注意力来度过困难时刻的技能",
        "适用场景": ["强烈的负面情绪", "想要自伤", "无法改变现状"],
        "steps": [
            {
                "step": 1,
                "title": "Activities（活动）",
                "description": "参加能分散注意力的活动",
                "guidance": "做你喜欢的事：看电影、运动、读书、游戏等。选择能吸引你注意力的事。"
            },
            {
                "step": 2,
                "title": "Contributing（奉献）",
                "description": "帮助别人或参与有意义的活动",
                "guidance": "做志愿者、帮助朋友或家人，参与社区活动。"
            },
            {
                "step": 3,
                "title": "Comparing（比较）",
                "description": "比较：你的处境与他人或更糟的情况",
                "guidance": "告诉自己这不是世界上最坏的情况。许多人经历过更困难的事。"
            },
            {
                "step": 4,
                "title": "Emotions（情绪）",
                "description": "用看电影、看视频等触发不同情绪",
                "guidance": "看喜剧让自己笑，看感人的故事体验不同的情绪。"
            },
            {
                "step": 5,
                "title": "Pushing away（推开）",
                "description": "暂时推开困难的想法和感受",
                "guidance": "告诉自己'我现在不处理这个，等等再想'，暂时转移注意力。"
            },
            {
                "step": 6,
                "title": "Thoughts（想法）",
                "description": "用其他想法替换痛苦的想法",
                "guidance": "做心算、背诗、唱歌等需要集中注意力的心理活动。"
            },
            {
                "step": 7,
                "title": "Sensations（感官）",
                "description": "用强烈的感官体验分散注意力",
                "guidance": "冰水、辣椒、刮胡子、香精油等强烈的感觉。"
            }
        ],
        "注意事项": "这是暂时度过危机的方式，不是解决问题的办法",
        "预期效果": "度过危机时刻，获得喘息机会"
    },

    "IMPROVE": {
        "name": "IMPROVE",
        "category": "distress_tolerance",
        "introduction": "改善当下时刻的技能，在无法改变情况时提升感受",
        "适用场景": ["无能为力", "被困于糟糕环境", "需要提升心情"],
        "steps": [
            {
                "step": 1,
                "title": "Imagery（想象）",
                "description": "在脑海中想象美好的场景",
                "guidance": "想象你最喜欢的地方、放松的时刻、美好的回忆。"
            },
            {
                "step": 2,
                "title": "Meaning（意义）",
                "description": "找出困难情况中的意义或学习",
                "guidance": "'这教会了我什么？' '这如何让我成长？' '这如何帮助他人？'"
            },
            {
                "step": 3,
                "title": "Prayer（祈祷）",
                "description": "祈祷或冥想（如适用的话）",
                "guidance": "不一定是宗教性的。可以是冥想、瑜伽、正念等精神实践。"
            },
            {
                "step": 4,
                "title": "Relaxation（放松）",
                "description": "进行放松活动",
                "guidance": "深呼吸、肌肉放松、洗澡、按摩等。"
            },
            {
                "step": 5,
                "title": "One thing in the moment（专注当下一件事）",
                "description": "专注于此刻的一件事，而不是整个问题",
                "guidance": "不想着整个问题，只关注当下的一个步骤或一个感受。"
            },
            {
                "step": 6,
                "title": "Vacation（度假）",
                "description": "给自己一个小的休息或暂停",
                "guidance": "即使不能去度假，也可以给自己一小段'心理假期'。"
            },
            {
                "step": 7,
                "title": "Encouragement（鼓励）",
                "description": "给自己积极的自我对话",
                "guidance": "'我可以度过这个。' '我很坚强。' '这只是暂时的。'"
            }
        ],
        "注意事项": "IMPROVE 是关于改善体验，不是否认问题",
        "预期效果": "改善困难时期的心态，增加韧性"
    },

    "利弊分析": {
        "name": "利弊分析",
        "category": "distress_tolerance",
        "introduction": "通过理性分析来做出困难决定的技能",
        "适用场景": ["纠结于决定", "想要自伤或冲动行为", "需要理性思考"],
        "steps": [
            {
                "step": 1,
                "title": "列出选项",
                "description": "明确你正在考虑的不同选择",
                "guidance": "例如：选项A、选项B或选项C。包括'不改变现状'作为一个选项。"
            },
            {
                "step": 2,
                "title": "分析每个选项的利弊",
                "description": "为每个选项列出优点和缺点",
                "guidance": "短期和长期都要考虑。包括对自己和他人的影响。"
            },
            {
                "step": 3,
                "title": "比较不同选项",
                "description": "比较每个选项的总体结果",
                "guidance": "哪个选项的优点最多，缺点最少？"
            },
            {
                "step": 4,
                "title": "考虑你的价值观",
                "description": "选择与你的价值观最一致的选项",
                "guidance": "这个决定是否符合你想成为的人？"
            }
        ],
        "注意事项": "利弊分析是理性工具，感受也很重要",
        "预期效果": "做出更理性的决定，减少冲动行为"
    },

    "激进接纳": {
        "name": "激进接纳",
        "category": "distress_tolerance",
        "introduction": "全然接受无法改变的痛苦和现实",
        "适用场景": ["无法改变的情况", "持续的痛苦", "需要放弃抵抗"],
        "steps": [
            {
                "step": 1,
                "title": "承认现实",
                "description": "完全承认现实是什么样的",
                "guidance": "停止说'这不应该发生'。说'这确实发生了'。"
            },
            {
                "step": 2,
                "title": "停止斗争",
                "description": "停止与现实的斗争",
                "guidance": "抵抗会增加痛苦。接纳不意味着同意，而是停止斗争。"
            },
            {
                "step": 3,
                "title": "允许悲伤",
                "description": "允许自己体验随之而来的悲伤或失望",
                "guidance": "这是自然的和必要的。不要试图避免这些情绪。"
            },
            {
                "step": 4,
                "title": "向前迈进",
                "description": "在接纳的基础上，找到继续生活的方式",
                "guidance": "接纳现实后，问自己：'现在我能做什么？'"
            }
        ],
        "注意事项": "激进接纳是一个过程，需要时间",
        "预期效果": "减少痛苦，增加心理灵活性"
    },

    # 情绪调节技能补充
    "相反行动": {
        "name": "相反行动",
        "category": "emotion_regulation",
        "introduction": "通过做与情绪相反的行动来改变情绪",
        "适用场景": ["不想做必要的事", "被恐惧阻止", "想逃避"],
        "steps": [
            {
                "step": 1,
                "title": "识别情绪",
                "description": "清楚地识别你的情绪",
                "guidance": "我感到恐惧、悲伤、愤怒还是内疚？"
            },
            {
                "step": 2,
                "title": "注意冲动",
                "description": "注意这个情绪想让你做什么",
                "guidance": "恐惧说'逃避'，悲伤说'躲起来'，愤怒说'攻击'。"
            },
            {
                "step": 3,
                "title": "做相反的事",
                "description": "做与你冲动相反的事",
                "guidance": "如果恐惧让你躲避，就去接近；如果愤怒让你尖叫，就保持冷静和友好。"
            },
            {
                "step": 4,
                "title": "坚持足够长",
                "description": "做足够长的时间直到情绪改变",
                "guidance": "通常需要持续30分钟或更长时间。耐心等待。"
            }
        ],
        "注意事项": "这个技能对恐惧、悲伤和有时愤怒特别有效",
        "预期效果": "改变情绪，增加动力"
    },

    "检查事实": {
        "name": "检查事实",
        "category": "emotion_regulation",
        "introduction": "通过检查你对情况的解读是否符合事实来调节情绪",
        "适用场景": ["过度反应", "灾难化思维", "焦虑发作"],
        "steps": [
            {
                "step": 1,
                "title": "识别想法",
                "description": "识别引发情绪的想法",
                "guidance": "写下你的自动想法。例如：'没人喜欢我' 或 '我会失败'。"
            },
            {
                "step": 2,
                "title": "寻找证据",
                "description": "寻找支持和反对这个想法的证据",
                "guidance": "证据：'我有朋友'、'我之前成功过'、'没人说不喜欢我'。"
            },
            {
                "step": 3,
                "title": "考虑替代解释",
                "description": "想想其他可能解释这个情况的方式",
                "guidance": "朋友没回应可能是很忙，不一定是不喜欢我。"
            },
            {
                "step": 4,
                "title": "得出平衡的结论",
                "description": "基于所有证据，得出更现实的想法",
                "guidance": "新想法：'我有一些朋友。有时他们很忙。我会成功的。'"
            }
        ],
        "注意事项": "目标不是积极思维，而是现实思维",
        "预期效果": "减少不必要的焦虑，更理性地看待情况"
    },

    "PLEASE技能": {
        "name": "PLEASE技能",
        "category": "emotion_regulation",
        "introduction": "通过照顾基本身体需求来增加情绪耐受力",
        "适用场景": ["情绪低落", "容易激惹", "需要增加心理韧性"],
        "steps": [
            {
                "step": 1,
                "title": "Physical illness（照顾生病）",
                "description": "治疗任何身体疾病或健康问题",
                "guidance": "看医生，按时服药，照顾身体症状。"
            },
            {
                "step": 2,
                "title": "Balanced eating（均衡饮食）",
                "description": "吃营养均衡的食物",
                "guidance": "不要跳餐，吃富含营养的食物而不是垃圾食品。"
            },
            {
                "step": 3,
                "title": "Avoid mood-altering substances（避免改变情绪的物质）",
                "description": "避免酒精、毒品和过量咖啡因",
                "guidance": "这些会波动你的情绪，使情绪调节更困难。"
            },
            {
                "step": 4,
                "title": "Sleep（睡眠）",
                "description": "获得足够的睡眠",
                "guidance": "尽量每晚睡7-9小时。保持规律的睡眠时间表。"
            },
            {
                "step": 5,
                "title": "Exercise（运动）",
                "description": "定期运动",
                "guidance": "每周至少150分钟的中等强度运动，或75分钟的高强度运动。"
            }
        ],
        "注意事项": "PLEASE不会解决所有问题，但会增加你的心理能力",
        "预期效果": "增加情绪耐受力和心理韧性"
    },

    "积极情绪清单": {
        "name": "积极情绪清单",
        "category": "emotion_regulation",
        "introduction": "建立积极情绪的'储蓄账户'以抵抗困难时期",
        "适用场景": ["抑郁情绪", "需要提升情绪", "为困难做准备"],
        "steps": [
            {
                "step": 1,
                "title": "列出愉快活动",
                "description": "列出让你感到快乐的事",
                "guidance": "包括各种活动：小事（喝咖啡）、中事（看电影）、大事（旅行）。"
            },
            {
                "step": 2,
                "title": "计划积极体验",
                "description": "提前计划这些活动",
                "guidance": "在日历上标记。确保你有东西期待。"
            },
            {
                "step": 3,
                "title": "定期参与",
                "description": "即使不想，也要定期参与这些活动",
                "guidance": "当你抑郁时，你最不想做的事通常是你最需要做的事。"
            },
            {
                "step": 4,
                "title": "增加喜悦",
                "description": "完全投入这些活动中享受它们",
                "guidance": "不要匆匆进行。暂时放下手机，真正沉浸其中。"
            }
        ],
        "注意事项": "小的积极体验也有帮助。不需要等待大的快乐时刻。",
        "预期效果": "增加快乐时刻，减少抑郁感"
    },

    # 正念技能补充
    "观察、描述、参与": {
        "name": "观察、描述、参与",
        "category": "mindfulness",
        "introduction": "三层正念技能，从被动观察到主动参与",
        "适用场景": ["情绪过载", "焦虑时的过度反应", "需要增加觉察"],
        "steps": [
            {
                "step": 1,
                "title": "观察（Observe）",
                "description": "成为你思想、感受和感官的观察者",
                "guidance": "就像看电视一样观察你的想法和感受。不要参与或评判，只是看。"
            },
            {
                "step": 2,
                "title": "描述（Describe）",
                "description": "用言语描述你观察到的",
                "guidance": "说出来或写下来：'我注意到焦虑的想法'、'我感到胸部紧张'。"
            },
            {
                "step": 3,
                "title": "参与（Participate）",
                "description": "完全投入当前的活动",
                "guidance": "完全沉浸于你正在做的事情中。全身心投入。"
            }
        ],
        "注意事项": "这三个步骤可以单独使用，也可以结合使用",
        "预期效果": "增加自我觉察，减少被情绪淹没的感觉"
    },

    "无评判态度": {
        "name": "无评判态度",
        "category": "mindfulness",
        "introduction": "观察想法和感受而不做出积极或消极的判断",
        "适用场景": ["自我批评", "完美主义", "自我憎恨"],
        "steps": [
            {
                "step": 1,
                "title": "注意评判",
                "description": "注意你自己何时在评判",
                "guidance": "听你的内心声音。'我很愚蠢' '我很糟糕' 这些都是评判。",
            },
            {
                "step": 2,
                "title": "放下评判",
                "description": "尝试简单地观察而不评判",
                "guidance": "用中立的方式重新表述：'我做了一个错误' 而不是 '我很糟糕'。",
            },
            {
                "step": 3,
                "title": "观察评判本身",
                "description": "当评判出现时，观察它就像观察天空中的云",
                "guidance": "想法来了，想法走了。你不需要信任它或与它斗争。",
            },
            {
                "step": 4,
                "title": "练习自我同情",
                "description": "用对待朋友的方式对待自己",
                "guidance": "如果朋友犯了错，你会说什么？对自己也这样说。",
            },
        ],
        "注意事项": "这需要大量练习。初期会很困难。",
        "预期效果": "减少自我批评，增加自我接纳",
    },

    # 补充缺失技能（与 SkillRecommender 匹配）
    "节律呼吸": {
        "name": "节律呼吸",
        "category": "mindfulness",
        "introduction": "通过有节奏的深呼吸来调节自主神经系统，缓解焦虑和紧张",
        "适用场景": ["焦虑", "紧张", "需要快速冷静"],
        "steps": [
            {
                "step": 1,
                "title": "找到舒适姿势",
                "description": "坐着或躺着，保持脊椎直立",
                "guidance": "放松肩膀，不要僵硬。闭上眼睛或微开。",
            },
            {
                "step": 2,
                "title": "吸气5秒",
                "description": "缓慢地用鼻子吸气，数到5",
                "guidance": "让空气充满腹部，然后是胸部。数到5：1-2-3-4-5。",
            },
            {
                "step": 3,
                "title": "呼气7秒",
                "description": "缓慢地用鼻子或嘴巴呼气，数到7",
                "guidance": "让气息自然流出，不要用力。数到7：1-2-3-4-5-6-7。",
            },
            {
                "step": 4,
                "title": "重复5分钟",
                "description": "持续这个呼吸模式约5分钟",
                "guidance": "如果数数困难，可以在吸气时想'平静'，呼气时想'放松'。",
            },
        ],
        "注意事项": "如果感到头晕，降低吸气/呼气的时间比例",
        "预期效果": "降低心率，缓解焦虑",
    },

    "正念观察": {
        "name": "正念观察",
        "category": "mindfulness",
        "introduction": "以观察者身份不加评判地注意当下的想法、感受和感官体验",
        "适用场景": ["思绪混乱", "被情绪淹没", "需要增加觉察"],
        "steps": [
            {
                "step": 1,
                "title": "选择观察对象",
                "description": "选择一种体验：呼吸、想法、身体感觉或周围环境",
                "guidance": "初学者建议从呼吸开始。",
            },
            {
                "step": 2,
                "title": "只是观察",
                "description": "注意它，但不要改变或评判",
                "guidance": "像一个科学家观察样本一样。只是记录你注意到的。",
            },
            {
                "step": 3,
                "title": "标注体验",
                "description": "给观察到的内容贴上标签",
                "guidance": "想法：'计划ing...''担忧ing...'；感受：'紧张''悲伤'。",
            },
            {
                "step": 4,
                "title": "温和带回",
                "description": "走神时，温和地把注意力带回观察对象",
                "guidance": "不要责备自己，这很正常。每一次带回都是练习。",
            },
        ],
        "注意事项": "不要试图控制或改变你观察到的",
        "预期效果": "增加觉察，减少被自动反应控制",
    },

    "剧烈运动": {
        "name": "剧烈运动",
        "category": "distress_tolerance",
        "introduction": "通过高强度运动释放能量，快速改变情绪状态",
        "适用场景": ["愤怒", "焦虑", "需要快速释放压力"],
        "steps": [
            {
                "step": 1,
                "title": "选择运动方式",
                "description": "选择你能立即做的运动",
                "guidance": "原地跑步、开合跳、俯卧撑、深蹲、上下楼梯等。",
            },
            {
                "step": 2,
                "title": "全力运动",
                "description": "以最大能力运动5-10分钟",
                "guidance": "让心跳加速，出汗，感觉身体在用力。",
            },
            {
                "step": 3,
                "title": "感觉身体",
                "description": "注意运动时的身体感觉",
                "guidance": "注意心跳、呼吸、肌肉的感觉。让注意力集中在身体上。",
            },
        ],
        "注意事项": "如果有心脏病或健康问题，选择低强度运动",
        "预期效果": "释放紧张情绪，产生内啡肽",
    },

    "冷水刺激": {
        "name": "冷水刺激",
        "category": "distress_tolerance",
        "introduction": "用冷水刺激面部或手部，激活潜水反射，快速降低心率和平静神经系统",
        "适用场景": ["恐慌发作", "强烈焦虑", "需要快速冷静"],
        "steps": [
            {
                "step": 1,
                "title": "准备冷水",
                "description": "准备可以淹没面部的冷水",
                "guidance": "用冷水洗脸，或准备一盆冰水。如果没有冰块，用很冷的水也可以。",
            },
            {
                "step": 2,
                "title": "深呼吸",
                "description": "先做几次深呼吸",
                "guidance": "放松，不要紧张。冷水只是暂时的刺激。",
            },
            {
                "step": 3,
                "title": "将脸浸入水中",
                "description": "将面部浸入冷水中30秒-1分钟",
                "guidance": "用鼻子呼吸，忍受一下。这种不适会很快过去。",
            },
        ],
        "注意事项": "有心脏病或呼吸问题的人谨慎使用",
        "预期效果": "30秒内心率下降，情绪强度降低",
    },

    "慢慢呼吸": {
        "name": "慢慢呼吸",
        "category": "mindfulness",
        "introduction": "通过放慢呼吸节奏来激活副交感神经系统，促进放松",
        "适用场景": ["紧张", "轻微焦虑", "需要放松"],
        "steps": [
            {
                "step": 1,
                "title": "坐姿舒适",
                "description": "坐直或半躺，让身体放松",
                "guidance": "松开紧身的衣服，把手放在舒适的位置。",
            },
            {
                "step": 2,
                "title": "延长呼气",
                "description": "呼气时间比吸气长",
                "guidance": "吸气数到4，呼气数到6或8。",
            },
            {
                "step": 3,
                "title": "专注呼吸",
                "description": "注意力集中在呼吸的感觉上",
                "guidance": "感受空气进入和离开身体的感觉。",
            },
        ],
        "注意事项": "如果感到头晕，稍微减少呼气时间",
        "预期效果": "平静神经系统，降低焦虑",
    },

    "安全空间想象": {
        "name": "安全空间想象",
        "category": "mindfulness",
        "introduction": "在内心想象一个让你感到完全安全和舒适的地方",
        "适用场景": ["焦虑", "恐惧", "需要内心平静"],
        "steps": [
            {
                "step": 1,
                "title": "选择你的安全空间",
                "description": "想一个让你感到安全、平静的地方",
                "guidance": "可以是真实的地方（童年住所、海滩）或想象的地方。",
            },
            {
                "step": 2,
                "title": "用五感想象",
                "description": "用所有感官详细想象这个空间",
                "guidance": "看到什么？听到什么？闻到什幺？触摸到什么？感觉如何？",
            },
            {
                "step": 3,
                "title": "停留片刻",
                "description": "在这个安全空间中停留几分钟",
                "guidance": "让自己完全沉浸其中，感受安全和平静。",
            },
        ],
        "注意事项": "如果无法想象可视化，用抽象的感觉也可以",
        "预期效果": "快速降低焦虑，获得内心平静",
    },

    "渐进式放松": {
        "name": "渐进式放松",
        "category": "mindfulness",
        "introduction": "通过逐步收紧和放松肌肉群来释放身体紧张",
        "适用场景": ["身体紧张", "焦虑", "难以入睡"],
        "steps": [
            {
                "step": 1,
                "title": "从脚开始",
                "description": "收紧脚部肌肉5秒，然后放松",
                "guidance": "卷起脚趾，感受紧张，然后完全放松，注意放松的感觉。",
            },
            {
                "step": 2,
                "title": "向上移动",
                "description": "对小腿、大腿、腹部、胸部、手臂、面部重复",
                "guidance": "每个部位收紧5秒，然后放松10秒。注意两者的区别。",
            },
            {
                "step": 3,
                "title": "全身放松",
                "description": "完成后，感受全身放松的状态",
                "guidance": "深呼吸几次，保持这种放松的感觉。",
            },
        ],
        "注意事项": "如果有受伤的部位，跳过那个部位",
        "预期效果": "释放身体紧张，促进放松和睡眠",
    },

    "正念享受": {
        "name": "正念享受",
        "category": "mindfulness",
        "introduction": "全身心投入地体验积极事物，充分感受美好时刻",
        "适用场景": ["快乐时光", "想要增强积极情绪", "需要感恩"],
        "steps": [
            {
                "step": 1,
                "title": "暂停并注意",
                "description": "当你感到愉快时，暂停并注意它",
                "guidance": "对自己说：'这一刻是美好的。'",
            },
            {
                "step": 2,
                "title": "全身心投入",
                "description": "完全沉浸在当前体验中",
                "guidance": "不要想其他事，也不要急于拍照或分享。只是感受。",
            },
            {
                "step": 3,
                "title": "品味愉悦感",
                "description": "注意积极情绪在身体中的感觉",
                "guidance": "注意微笑的感觉、胸口的温暖、身体的轻盈。",
            },
        ],
        "注意事项": "不要评判这个享受是否'应该'",
        "预期效果": "增强积极情绪的持续性和深度",
    },

    "感恩记录": {
        "name": "感恩记录",
        "category": "mindfulness",
        "introduction": "通过书写记录每天值得感恩的事情，培养积极心态",
        "适用场景": ["情绪低落", "负面思维", "想要改变视角"],
        "steps": [
            {
                "step": 1,
                "title": "准备感恩日记",
                "description": "选择一个本子或应用来记录",
                "guidance": "可以是纸质笔记本或手机备忘录。每天记录。",
            },
            {
                "step": 2,
                "title": "列出3件感恩的事",
                "description": "每天写下3件值得感恩的事",
                "guidance": "从小事开始：好天气、美味的咖啡、朋友的问候。",
            },
            {
                "step": 3,
                "title": "描述细节",
                "description": "写下为什么这件事值得感恩",
                "guidance": "'我感恩朋友的消息，因为这让我感到被关心。'",
            },
        ],
        "注意事项": "不要为了完成任务而写，要真诚地感受",
        "预期效果": "培养积极视角，改善整体幸福感",
    },

    "分享快乐": {
        "name": "分享快乐",
        "category": "interpersonal",
        "introduction": "将积极情绪和体验与他人分享，增进关系",
        "适用场景": ["感到快乐", "想要加强关系", "想要传递正能量"],
        "steps": [
            {
                "step": 1,
                "title": "识别快乐时刻",
                "description": "当你感到快乐时，注意到它",
                "guidance": "可以是小的快乐（一杯好咖啡）或大的快乐（成功）。",
            },
            {
                "step": 2,
                "title": "选择分享对象",
                "description": "选择你想与之分享的人",
                "guidance": "可以是朋友、家人或同事。谁会对你的快乐感兴趣？",
            },
            {
                "step": 3,
                "title": "真诚分享",
                "description": "分享你的快乐经历和感受",
                "guidance": "'我今天成功完成了项目，想和你分享这个好消息！'",
            },
        ],
        "注意事项": "分享时考虑对方的情况，不要炫耀",
        "预期效果": "增进关系，放大快乐感",
    },

    "价值澄清": {
        "name": "价值澄清",
        "category": "mindfulness",
        "introduction": "识别和明确对你来说最重要的事物和原则",
        "适用场景": ["感到迷茫", "需要做决定", "想要更了解自己"],
        "steps": [
            {
                "step": 1,
                "title": "列出重要领域",
                "description": "想想生活中重要的方面",
                "guidance": "如家庭、友谊、学习、健康、创造力、诚实等。",
            },
            {
                "step": 2,
                "title": "识别核心价值",
                "description": "哪些是你最看重的？",
                "guidance": "问自己：'如果没人知道，我会选择什么？' '我希望被记住是什么样子？'",
            },
            {
                "step": 3,
                "title": "与行为对照",
                "description": "检查你的行为是否与价值观一致",
                "guidance": "我今天的选择是否符合我最重要的价值观？",
            },
        ],
        "注意事项": "没有错误的价值观，重要的是诚实面对自己",
        "预期效果": "增加自我了解，做出更符合内心的决定",
    },

    "正念冥想": {
        "name": "正念冥想",
        "category": "mindfulness",
        "introduction": "通过有意识的、不评判的注意来培养当下的觉察",
        "适用场景": ["压力", "焦虑", "需要内心平静"],
        "steps": [
            {
                "step": 1,
                "title": "找安静地方",
                "description": "选择一个安静、舒适的地方坐下",
                "guidance": "不需要盘腿坐，椅子也可以。保持背部挺直但不僵硬。",
            },
            {
                "step": 2,
                "title": "设定时间",
                "description": "从5分钟开始，逐渐增加",
                "guidance": "可以用手机计时，开始时不要太久。",
            },
            {
                "step": 3,
                "title": "关注呼吸",
                "description": "将注意力集中在呼吸上",
                "guidance": "注意呼吸的自然节奏。不要控制它，只是观察。",
            },
            {
                "step": 4,
                "title": "处理走神",
                "description": "发现走神时，温和地带回注意力",
                "guidance": "不要评判自己，这正是练习。带回注意力到呼吸上。",
            },
        ],
        "注意事项": "初学者走神是正常的，坚持练习会改善",
        "预期效果": "减少压力，提高专注力和情绪调节能力",
    },

    "情绪调节": {
        "name": "情绪调节",
        "category": "emotion_regulation",
        "introduction": "了解情绪的触发因素，用健康的方式管理情绪反应",
        "适用场景": ["情绪波动", "容易被触发", "想要更好地管理情绪"],
        "steps": [
            {
                "step": 1,
                "title": "识别触发点",
                "description": "注意什么情况会触发你的情绪",
                "guidance": "记录引发强烈情绪的情境、想法或事件。",
            },
            {
                "step": 2,
                "title": "觉察早期信号",
                "description": "学会识别情绪即将来临的早期信号",
                "guidance": "身体感觉（心跳加速、肌肉紧张）通常是第一个信号。",
            },
            {
                "step": 3,
                "title": "选择调节策略",
                "description": "在情绪升级前使用技能",
                "guidance": "可以是深呼吸、暂停、接地技术或暂时离开情境。",
            },
            {
                "step": 4,
                "title": "反思和调整",
                "description": "情绪平复后回顾这次经历",
                "guidance": "什么有效？什么可以改进？为下次做得更好。",
            },
        ],
        "注意事项": "调节不是压抑，而是更智慧地回应",
        "预期效果": "减少情绪失控，更自信地应对挑战",
    },
}


def get_skill_info(skill_name: str) -> Dict:
    """
    获取技能详细信息
    :param skill_name: 技能名称
    :return: 技能信息字典
    """
    return SKILLS_DATABASE.get(
        skill_name,
        {
            "name": skill_name,
            "category": "other",
            "introduction": "DBT技能",
            "steps": [],
        },
    )


def get_all_skills() -> List[str]:
    """
    获取所有技能名称列表
    :return: 技能名称列表
    """
    return list(SKILLS_DATABASE.keys())


def get_skills_by_category(category: str) -> List[str]:
    """
    根据分类获取技能列表
    :param category: 分类名称
    :return: 技能名称列表
    """
    return [
        name
        for name, info in SKILLS_DATABASE.items()
        if info.get("category") == category
    ]


def get_skill_steps(skill_name: str) -> List[str]:
    """
    获取技能的步骤guidance文本列表
    :param skill_name: 技能名称
    :return: 步骤guidance文本列表
    """
    skill_info = SKILLS_DATABASE.get(skill_name)
    if not skill_info:
        return []
    steps = skill_info.get("steps", [])
    return [step.get("guidance", "") for step in steps]
