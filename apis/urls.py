from django.urls import path
from .views import *

urlpatterns = [
    path('client/register/', ClientCreateView.as_view()),
    path('owner/register/', OwnerCreateView.as_view()),
    path('staff/register/', StaffView.as_view()),
    path('staff/<str:staffno>/', StaffView.as_view()),
    path('branch/', BranchCreateView.as_view()),
    path('lease/create/', LeaseCreateView.as_view()),
    path('property/register/', PropertyCreateView.as_view()),
]