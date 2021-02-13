"""exposeee_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import re_path, path, include
from core.views import ExposeUploadView, ExportView
from core.api import (
    ExposeUploadFileView, ExposeListView,
    ExposeBrowserStorageView, ExportExposesView, DeleteExposesView,
)
from rest_framework_simplejwt import views as jwt_views
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/v1/expose/', ExposeUploadView.as_view(), name='v1-expose'),
    path('api/v1/export/', ExportView.as_view(), name='v1-expose-export'),
    path(
        r'api/v2/expose/upload_file/',
        ExposeUploadFileView.as_view(),
        name='v2_expose_upload_file',
    ),
    path(
        r'api/v2/expose/list/',
        ExposeListView.as_view(),
        name='v2_expose_list',
    ),
    path(
        r'api/v2/expose/save_from_browser_storage/',
        ExposeBrowserStorageView.as_view(),
        name='v2_expose_save_browser_storage',
    ),
    path(
        r'api/v2/expose/export/',
        ExportExposesView.as_view(),
        name='v2_expose_export',
    ),
    path(
        r'api/v2/expose/delete/',
        DeleteExposesView.as_view(),
        name='v2_expose_delete',
    ),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('memba-auth/', include('dj_rest_auth.urls')),
    path('memba-auth/registration/', include('dj_rest_auth.registration.urls')),
    path(
        'memba-auth/account-confirm-email/',
        VerifyEmailView.as_view(),
        name='account_email_verification_sent'
    ),
]
