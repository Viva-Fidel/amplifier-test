from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, ImportMaterialsView, MaterialViewSet

router = SimpleRouter()
router.register(r"materials", MaterialViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("import_materials/", ImportMaterialsView.as_view(), name="import-materials"),
]
