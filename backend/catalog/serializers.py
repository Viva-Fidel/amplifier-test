from rest_framework import serializers

from .models import Category, Material
from .validators import ValidateXLSX


class MaterialSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = ["id", "name", "category", "code", "cost"]

    def get_category(self, obj):
        return obj.category.name if obj.category else None


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    materials = MaterialSerializer(many=True, read_only=True)
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "code", "parent", "children", "materials"]

    def get_children(self, obj):
        return CategorySerializer(obj.children, many=True).data

    def get_parent(self, obj):
        return obj.parent.name if obj.parent else None


class FlatCategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "code", "parent"]

    def get_parent(self, obj):
        return obj.parent.name if obj.parent else None


class TreeCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    materials = MaterialSerializer(many=True, read_only=True)
    parent = serializers.SerializerMethodField()
    materials_cost = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "code",
            "parent",
            "children",
            "materials",
            "materials_cost",
        ]

    def get_children(self, obj):
        return CategorySerializer(obj.children, many=True).data

    def get_parent(self, obj):
        return obj.parent.name if obj.parent else None

    def get_materials_cost(self, obj):
        return self.calculate_materials_cost(obj)

    # Вычисление общей стоимости для текущей категории и всех её подкатегорий
    def calculate_materials_cost(self, category):
        category_cost = sum(material.cost for material in category.materials.all())

        for child in category.children.all():
            category_cost += self.calculate_materials_cost(child)

        return category_cost


class ImportMaterialsSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[ValidateXLSX()])
