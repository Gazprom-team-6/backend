from django.urls import include, path
from rest_framework import routers

from company import views

app_name = "company"

router_v1 = routers.DefaultRouter()

router_v1.register(
    "department",
    views.DepartmentViewSet,
    basename="department"
)
router_v1.register(
    "product",
    views.ProductViewSet,
    basename="product"
)
router_v1.register(
    "team",
    views.TeamViewSet,
    basename="team"
)

urlpatterns = [
    path("", include(router_v1.urls)),
]
