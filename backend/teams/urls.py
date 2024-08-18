from django.urls import include, path
from rest_framework import routers

from teams import views

app_name = "team"

router_v1 = routers.DefaultRouter()

router_v1.register("team", views.TeamViewSet, basename="team")

urlpatterns = [
    path("", include(router_v1.urls)),
]
