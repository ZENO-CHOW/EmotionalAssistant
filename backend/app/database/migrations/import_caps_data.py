"""
导入CAPS情绪图片数据
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.database.connection import SessionLocal, init_db
from app.database.models import EmotionImage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_category_from_filename(filename: str) -> str:
    """根据文件名判断类别"""
    if filename.startswith("_"):
        return "negative"
    elif filename.startswith("1"):
        return "positive"
    elif filename.startswith("2"):
        return "neutral"
    return "unknown"


def import_caps_data():
    """导入CAPS图片数据"""
    logger.info("=" * 50)
    logger.info("开始导入CAPS情绪图片数据...")
    logger.info("=" * 50)

    init_db()

    base_dir = Path(__file__).parent.parent.parent.parent / "static/images/caps"

    if not base_dir.exists():
        logger.error(f"图片目录不存在: {base_dir}")
        return

    db = SessionLocal()

    try:
        db.query(EmotionImage).delete()
        db.commit()
        logger.info("✓ 清空现有数据")

        categories = {
            "positive": {"valence": 6.0, "arousal": 5.0, "dominance": 6.0},
            "neutral": {"valence": 5.0, "arousal": 5.0, "dominance": 5.0},
            "negative": {"valence": 3.0, "arousal": 6.0, "dominance": 3.0},
        }

        success_count = 0
        error_count = 0

        for category in ["positive", "neutral", "negative"]:
            category_dir = base_dir / category
            if not category_dir.exists():
                continue

            for filename in sorted(os.listdir(category_dir)):
                if not filename.endswith(".jpg"):
                    continue

                try:
                    name_without_ext = filename.replace(".jpg", "")
                    image_id = name_without_ext

                    file_path = f"/static/images/caps/{category}/{filename}"

                    vad_values = categories.get(
                        category, {"valence": 5.0, "arousal": 5.0, "dominance": 5.0}
                    )

                    image = EmotionImage(
                        image_id=image_id,
                        name=filename,
                        category=category,
                        valence=vad_values["valence"],
                        arousal=vad_values["arousal"],
                        dominance=vad_values["dominance"],
                        file_path=file_path,
                    )

                    db.add(image)
                    success_count += 1

                except Exception as e:
                    logger.error(f"导入 {filename} 失败: {str(e)}")
                    error_count += 1
                    continue

        db.commit()

        logger.info("=" * 50)
        logger.info(f"✓ 导入完成!")
        logger.info(f"  成功: {success_count} 条")
        logger.info(f"  失败: {error_count} 条")
        logger.info("=" * 50)

        positive_count = (
            db.query(EmotionImage).filter(EmotionImage.category == "positive").count()
        )
        negative_count = (
            db.query(EmotionImage).filter(EmotionImage.category == "negative").count()
        )
        neutral_count = (
            db.query(EmotionImage).filter(EmotionImage.category == "neutral").count()
        )

        logger.info("分类统计:")
        logger.info(f"  正性图片: {positive_count}")
        logger.info(f"  负性图片: {negative_count}")
        logger.info(f"  中性图片: {neutral_count}")
        logger.info(f"  总计: {positive_count + negative_count + neutral_count}")

    except Exception as e:
        logger.error(f"导入过程出错: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import_caps_data()
