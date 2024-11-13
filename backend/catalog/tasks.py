import logging
import os

import pandas as pd
from catalog.models import Category, Material
from celery import shared_task
from django.db import transaction

logger = logging.getLogger(__name__)


@shared_task
def import_materials_task(file_path):
    """Читает Excel файл, обрабатывает данные и создает соответствующие
    объекты Category и Material в базе данных"""
    try:
        data = pd.read_excel(file_path)

        existing_categories = {
            (category.name, category.parent.name if category.parent else None): category
            for category in Category.objects.select_related("parent")
        }

        new_categories = []
        materials_to_create = []

        for _, row in data.iterrows():
            category_name = row["Category"]
            category_code = row["CategoryCode"]
            parent_category_name = (
                row["ParentCategory"]
                if "ParentCategory" in row and pd.notna(row["ParentCategory"])
                else None
            )

            category_key = (category_name, parent_category_name)
            if category_key in existing_categories:
                category = existing_categories[category_key]
            else:
                parent_category = existing_categories.get((parent_category_name, None))
                category = Category(
                    name=category_name, code=category_code, parent=parent_category
                )
                new_categories.append(category)
                existing_categories[category_key] = category

            materials_to_create.append(
                Material(
                    name=row["MaterialName"],
                    category=category,
                    code=row["MaterialCode"],
                    cost=row["MaterialCost"],
                )
            )

        with transaction.atomic():
            if new_categories:
                Category.objects.bulk_create(new_categories)
            Material.objects.bulk_create(materials_to_create)

        logger.info("Импорт данных завершен успешно")
        return "Загрузка завершена"

    except Exception as e:
        logger.error(f"Ошибка при импорте данных: {e}")
        raise

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Файл {file_path} удален после импорта")
