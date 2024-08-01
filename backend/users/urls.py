from django.urls import include, path
from users import views

urlpatterns = [
    path('password-reset/', views.PasswordResetView.as_view()),
    path('auth/', include('djoser.urls.jwt')),
]