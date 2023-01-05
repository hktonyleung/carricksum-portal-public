
from django.urls import path
from . import views
from .views import BranchesListView, BranchesCreateView, BranchUpdateView, BranchDeleteView, BranchUpdateSpatialView

app_name = 'branches'

urlpatterns = [
    path('', views.index, name="branches-index"),
    path('create', BranchesCreateView.as_view(), name='branches-create'),
    path('update/<str:pk>/', BranchUpdateView.as_view(), name='branches-update'),   
    path('update/spatial/<str:pk>/', BranchUpdateSpatialView.as_view(), name='branches-update-spatial'), 
    path('manage', BranchesListView.as_view(), name='branches-manage'),
    path('delete/<str:pk>/', BranchDeleteView.as_view(), name='branches-delete'),
]