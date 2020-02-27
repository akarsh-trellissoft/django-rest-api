from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from core.views import CustomerViewSet,ProfessionViewSet,DatesheetViewSet,DocumentViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('customers', CustomerViewSet,basename="customer")
router.register('professions', ProfessionViewSet)
router.register('date-sheets', DatesheetViewSet)
router.register('documents', DocumentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
]
