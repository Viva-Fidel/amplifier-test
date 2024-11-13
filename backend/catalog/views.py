from django.core.files.storage import default_storage
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Material
from .serializers import (
    CategorySerializer,
    FlatCategorySerializer,
    ImportMaterialsSerializer,
    MaterialSerializer,
    TreeCategorySerializer,
)
from .tasks import import_materials_task


# Create your views here.
class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=["get"], url_path="categories-list")
    def categories_list(self, request):
        queryset = self.get_queryset()
        serializer = FlatCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="categories-tree")
    def categories_tree(self, request):
        queryset = self.get_queryset()
        serializer = TreeCategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ImportMaterialsView(APIView):
    def post(self, request):
        serializer = ImportMaterialsSerializer(data=request.FILES)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data["file"]
        file_path = default_storage.save("tmp/" + file.name, file)

        import_materials_task.delay(file_path)

        return Response(
            {"status": "Загрузка файла началась"}, status=status.HTTP_202_ACCEPTED
        )
