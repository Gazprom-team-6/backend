from django.urls import include, path
from rest_framework import routers

from departments import views

app_name = "department"

router_v1 = routers.DefaultRouter()


router_v1.register(
    "department",
    views.DepartmentViewSet,
    basename="department"
)

urlpatterns = [
    path("", include(router_v1.urls)),
]
