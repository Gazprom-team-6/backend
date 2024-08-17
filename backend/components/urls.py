from django.urls import include, path
from rest_framework import routers

from components import views

app_name = "component"

router_v1 = routers.DefaultRouter()

router_v1.register("component", views.ComponentViewSet, basename="component")

urlpatterns = [
    path("", include(router_v1.urls)),
]
