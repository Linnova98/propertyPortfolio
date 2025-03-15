from django.urls import path
from . import views

urlpatterns = [
    path('', views.PorfolioOverview, name="portfolio-overview"),
    path('create/', views.add_instances, name='add-instances'),
    path('all/', views.view_instances, name='view-instances'),
    path('read/<int:pk>/', views.view_instance, name='view-instance'),
    path('update/<int:pk>/', views.update_instances, name='update-instances'),
    path('<int:pk>/delete/', views.delete_instances, name='delete-instances'),
]
