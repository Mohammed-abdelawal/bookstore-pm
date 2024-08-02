from django.urls import path, include
from core.views import RegisterView, BookViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("books", BookViewSet, basename="books")


urlpatterns = [
    path("", include(router.urls)),
    path("user/register/", RegisterView.as_view(), name="register"),
    path("user/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
