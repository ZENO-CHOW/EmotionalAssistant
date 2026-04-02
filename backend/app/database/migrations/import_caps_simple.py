"""
简化版：直接从文件导入图片数据
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


def import_from_files():
    """从文件系统导入图片数据"""
    logger.info("=" * 50)
    logger.info("从文件系统导入CAPS图片数据...")
    logger.info("=" * 50)

    init_db()
    db = SessionLocal()

    try:
        # 清空现有数据
        db.query(EmotionImage).delete()
        db.commit()

        # 图片目录
        base_dir = Path(__file__).parent.parent.parent.parent / "static/images/caps"

        # 默认VAD值（基于类别）
        default_vad = {
            'positive': {'valence': 7.0, 'arousal': 6.0, 'dominance': 6.5},
            'negative': {'valence': 3.0, 'arousal': 6.5, 'dominance': 4.0},
            'neutral': {'valence': 5.0, 'arousal': 4.5, 'dominance': 5.5}
        }

        success_count = 0

        for category in ['positive', 'negative', 'neutral']:
            category_dir = base_dir / category
            if not category_dir.exists():
                logger.warning(f"目录不存在: {category_dir}")
                continue

            files = list(category_dir.glob('*.jpg'))
            logger.info(f"处理 {category}: {len(files)} 张图片")

            for file_path in files:
                # 从文件名提取image_id
                image_id = file_path.stem  # 不含扩展名

                # 创建记录
                image = EmotionImage(
                    image_id=image_id,
                    name=image_id,
                    category=category,
                    valence=default_vad[category]['valence'],
                    arousal=default_vad[category]['arousal'],
                    dominance=default_vad[category]['dominance'],
                    file_path=f"/static/images/caps/{category}/{file_path.name}"
                )

                db.add(image)
                success_count += 1

            db.commit()
            logger.info(f"✓ {category}: 导入 {len(files)} 张")

        logger.info("=" * 50)
        logger.info(f"导入完成！总计: {success_count} 张")
        logger.info("=" * 50)

        # 统计
        for cat in ['positive', 'negative', 'neutral']:
            count = db.query(EmotionImage).filter(EmotionImage.category == cat).count()
            logger.info(f"  {cat}: {count}")

    except Exception as e:
        logger.error(f"导入失败: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import_from_files()
