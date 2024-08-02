from django.urls import path, include
from core.views import RegisterView, BookViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register("books", BookViewSet, basename="books")

schema_view = get_schema_view(
    openapi.Info(
        title="BookStore API",
        default_version="v1",
        description="API documentation for the BookStore application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mohammedabdelawaldeveloper@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],  # Ensure no basic auth
)


urlpatterns = [
    # core system views
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("user/register/", RegisterView.as_view(), name="register"),
    path("user/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # swagger urls
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger.yaml", schema_view.without_ui(cache_timeout=0), name="schema-yaml"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


if settings.DEBUG:  # TODO handle production storage
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
