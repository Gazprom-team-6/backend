from django.urls import include, path
from rest_framework import routers

from products import views

app_name = "product"

router_v1 = routers.DefaultRouter()

router_v1.register(
    "product",
    views.ProductViewSet,
    basename="product"
)

urlpatterns = [
    path("", include(router_v1.urls)),
]
