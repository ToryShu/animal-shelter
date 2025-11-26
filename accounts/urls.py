from django.urls import path
from .views import user_list, user_edit, user_delete

urlpatterns = [
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/edit/', user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', user_delete, name='user_delete'),
]
