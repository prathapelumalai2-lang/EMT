from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormViewSet, FieldViewSet, EmployeeViewSet, RegisterView, ProfileView, ChangePasswordView, IndexView

router = DefaultRouter()
router.register('forms', FormViewSet)
router.register('fields', FieldViewSet)
router.register('employees', EmployeeViewSet)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view()),
    path('api/profile/', ProfileView.as_view()),
    path('api/change-password/', ChangePasswordView.as_view()),
]