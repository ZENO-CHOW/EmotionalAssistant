"""
DBT技能API路由
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import logging

from app.dbt.skills import (
    SKILLS_DATABASE,
    get_skill_info,
    get_all_skills,
    get_skills_by_category
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/dbt/skills")
async def get_skills(
    category: Optional[str] = Query(None, description="技能分类: distress_tolerance/mindfulness/emotion_regulation/interpersonal")
):
    """
    获取DBT技能列表

    如果指定category，返回该分类下的技能；否则返回所有技能
    """
    try:
        if category:
            # 获取指定分类的技能
            skill_names = get_skills_by_category(category)
            skills = [get_skill_info(name) for name in skill_names]
        else:
            # 获取所有技能
            skill_names = get_all_skills()
            skills = [get_skill_info(name) for name in skill_names]

        return {
            "success": True,
            "count": len(skills),
            "category": category,
            "skills": skills
        }

    except Exception as e:
        logger.error(f"获取技能列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取技能列表失败: {str(e)}")


@router.get("/dbt/skills/{skill_name}")
async def get_skill_detail(skill_name: str):
    """
    获取指定技能的详细信息
    """
    try:
        skill = get_skill_info(skill_name)

        if not skill or not skill.get('steps'):
            raise HTTPException(status_code=404, detail=f"技能不存在: {skill_name}")

        return {
            "success": True,
            "skill": skill
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取技能详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取技能详情失败: {str(e)}")


@router.get("/dbt/categories")
async def get_categories():
    """
    获取所有技能分类及其统计
    """
    try:
        categories = {
            "distress_tolerance": {
                "name": "痛苦耐受",
                "name_en": "Distress Tolerance",
                "description": "在无法改变困难情况时，度过危机时刻的技能",
                "skills": get_skills_by_category("distress_tolerance")
            },
            "mindfulness": {
                "name": "正念",
                "name_en": "Mindfulness",
                "description": "活在当下，觉察和接纳的技能",
                "skills": get_skills_by_category("mindfulness")
            },
            "emotion_regulation": {
                "name": "情绪调节",
                "name_en": "Emotion Regulation",
                "description": "理解和管理情绪的技能",
                "skills": get_skills_by_category("emotion_regulation")
            },
            "interpersonal": {
                "name": "人际效能",
                "name_en": "Interpersonal Effectiveness",
                "description": "有效沟通和维护关系的技能",
                "skills": get_skills_by_category("interpersonal")
            }
        }

        # 添加统计信息
        for key, cat in categories.items():
            cat["count"] = len(cat["skills"])

        return {
            "success": True,
            "categories": categories,
            "total_skills": len(get_all_skills())
        }

    except Exception as e:
        logger.error(f"获取分类失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取分类失败: {str(e)}")
