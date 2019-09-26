"""eCall_SOS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from DeviceManage.views import DevicesListViewSet, SosGpsListViewSet, SosContactPersonListViewSet, ReceiveSosView, SendSosContactPersonViewSet
router = DefaultRouter()

# 配置devices的url
router.register(r'devices', DevicesListViewSet, base_name="devices")

# 配置sosgps的url
router.register(r'sosgps', SosGpsListViewSet, base_name="sosgps")

router.register(r'soscontactperson', SosContactPersonListViewSet, base_name="soscontactperson")

router.register(r'sendsoscontactperson', SendSosContactPersonViewSet, base_name="sendsoscontactperson")

# 重要的是如下三行
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'docs/', include_docs_urls(title="eCall_SOS")),
    url(r'^docs/', schema_view, name="docs"), # swaggerAPI文档
    url(r'^', include(router.urls)),
    url(r'^devices/receivesos', ReceiveSosView.as_view(), name="receivesos"),
]
