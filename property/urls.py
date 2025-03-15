from . import views
from django.urls import path

urlpatterns = [
    path('', views.PropertyOverview, name="property-overview"),
    path('create/', views.add_items, name='add-items'),
    path('all/', views.view_items, name='view-items'),
    path('read/<int:pk>/', views.view_item, name='view-item'),
    path('update/<int:pk>/', views.update_items, name='update-items'),
    path('<int:pk>/delete/', views.delete_items, name='delete-items'),
]
