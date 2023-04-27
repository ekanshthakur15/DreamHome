from django.urls import path
from .views import *

urlpatterns = [
    path('client/register/', ClientCreateView.as_view()),# post client
    path('owner/register/', OwnerCreateView.as_view()),  # post client
    path('staff/register/', StaffView.as_view()),  # post client
    path('staff/<str:staffno>/', StaffView.as_view()),  # post staff
    path('branch/', BranchCreateView.as_view()),  # post branch
    path('lease/create/', LeaseCreateView.as_view()),  # post lease
    path('property/register/', PropertyCreateView.as_view()),  # post property
    path('branch/<str:br_id>/', BranchDetailView.as_view()), # get branch detail
    path('property_search/', PropertyListView.as_view()),
    path('property_detail/<str:pnum>/', PropertyDetailView.as_view()), #to get the property detail
    path('branch_list/', BranchListView.as_view()),
]