"""
干预引导AGENT提示词模板
"""

INTERVENTION_AGENT_PROMPT = """你是一个专业的情绪干预引导助手。你的主要职责是：

1. **紧急情况处理**：对危机情况返回温暖、支持性的规则化响应
2. **技能引导**：多步骤引导用户练习DBT技能
3. **效果评估**：帮助用户评估技能练习前后的情绪变化
4. **对话总结**：生成今日对话的简要5. **结束总结
判断**：决定是否继续对话或结束

工作原则：
- 始终保持温暖、支持性的语气
- 优先处理紧急情况
- 引导技能练习时，要循序渐进
- 效果评估要客观、中立
- 结束时给出有价值的建议

记住：如果用户表达自我伤害或自杀想法，立即引导寻求专业帮助。"""


GUIDANCE_PROMPT = """现在我们来练习「{skill_name}」。

{skill_introduction}

**步骤 {current_step}/{total_steps}**：{step_title}

{step_description}

请按以下指导进行：
{step_guidance}

准备好了吗？完成后告诉我你的感受。"""


EFFECTIVENESS_EVALUATION_PROMPT = """用户刚刚完成了技能练习。

练习前情绪强度：{before_intensity}
练习后情绪强度：{after_intensity}
技能名称：{skill_name}

请评估：
1. 技能效果：有效（强度降低2分以上）/一般（强度变化1-2分）/无效（强度无变化或增加）
2. 用户参与度：高/中/低
3. 建议的下一步

以JSON格式返回：
{{
    "effectiveness": "有效|一般|无效",
    "user_engagement": "高|中|低",
    "suggestion": "继续学习|尝试其他|建议休息",
    "recommend_skill": "建议学习的下一个技能",
    "summary": "简要总结这次对话"
}}"""


SESSION_SUMMARY_PROMPT = """根据以下对话内容，生成一段简要的今日对话总结：

对话历史：
{conversation_history}

今日情绪状态：
{emotion_summary}

练习的技能：
{skills_practiced}

效果评估结果：
{effectiveness}

请用2-3句话总结这次对话的关键内容和收获。"""


SKILL_CONFIRMATION_PROMPT = """我推荐你尝试「{skill_name}」。

{skill_introduction}

这个技能包含 {steps_count} 个步骤，练习时间约 5-10 分钟。

你愿意尝试这个技能吗？"""


EVALUATION_REQUEST_PROMPT = (
    """你现在感觉怎么样？请用一个数字（1-10）来表示你的情绪强度，10表示最强烈。"""
)


FOLLOW_UP_PROMPT = """请告诉我，你现在的情绪强度是多少？（1-10分，10分最强烈）

这个分数和练习前相比有什么变化吗？"""


NEXT_STEP_PROMPT = """根据刚才的评估，我建议：{suggestion}

{specific_advice}

你还想继续学习其他技能，还是今天就到这里？"""


CLOSING_PROMPT = """感谢你今天的分享和练习。

今日总结：
{summary}

希望这些技能对你有帮助。记住，情绪管理是一个持续的过程，多练习会越来越熟练。

如果之后还有需要，随时可以回来找我。

祝你今天愉快！我们下次再见。"""


ALTERNATIVE_SKILL_PROMPT = """没关系，这个技能可能不太适合你现在的状态。

根据你的情绪类型（{emotion_type}），我推荐尝试「{alternative_skill}」。

你想试试这个替代技能吗？"""
