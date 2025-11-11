"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
import os


def serve_mkdocs(request, path=""):
    """Serve MkDocs documentation with proper handling of paths"""
    docs_root = settings.BASE_DIR.parent / "site"

    # If path is empty or ends with /, serve index.html
    if not path or path.endswith("/"):
        path = (path or "") + "index.html"

    # Check if file exists, otherwise serve index.html (for SPA routing)
    full_path = os.path.join(docs_root, path)
    if not os.path.exists(full_path):
        path = "index.html"

    return serve(request, path, document_root=docs_root)


urlpatterns = [
    path("admin/", admin.site.urls),
    # MkDocs documentation (must come early to avoid Vue catch-all)
    re_path(r"^docs/(?P<path>.*)$", serve_mkdocs, name="mkdocs-path"),
    path("docs/", serve_mkdocs, name="mkdocs"),
    # OpenAPI/Swagger documentation endpoints (must come before api/ include)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # API routes
    path("api/", include("api.urls")),
]

# Serve static files in development
if settings.DEBUG:
    # Serve Vue assets from /assets/ path
    urlpatterns += [
        re_path(
            r"^assets/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.BASE_DIR.parent / "dist" / "assets",
            },
        ),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve Vue app for all other routes (must be last)
urlpatterns += [
    re_path(r"^.*$", TemplateView.as_view(template_name="index.html"), name="vue-app"),
]
