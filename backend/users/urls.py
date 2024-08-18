from django.urls import include, path
from rest_framework import routers

from users import views

app_name = "users"

router_v1 = routers.DefaultRouter()

router_v1.register("", views.UserViewSet, basename="users")


urlpatterns = [
    path("password-reset/", views.PasswordResetView.as_view()),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(router_v1.urls)),
]
