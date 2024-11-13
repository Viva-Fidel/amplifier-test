from rest_framework import serializers


class ValidateXLSX:
    """Валидатор проверки файла на расширение xlsx"""

    def __call__(self, data):
        if not data.name.endswith(".xlsx"):
            raise serializers.ValidationError(
                "Некорректный формат файла. Разрешены только файлы с расширением .xlsx"
            )
