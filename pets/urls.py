from django.urls import path
from . import views

app_name = 'pets'

    
urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path('animal/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animal/<int:pk>/adopt/', views.adopt_animal, name='adopt_animal'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    # Admin panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/animals/', views.admin_animals, name='admin_animals'),
    path('admin-panel/animals/add/', views.admin_animal_create, name='admin_animal_create'),
    path('admin-panel/animals/<int:animal_id>/edit/', views.admin_animal_edit, name='admin_animal_edit'),
    path('admin-panel/animals/<int:animal_id>/delete/', views.admin_animal_delete, name='admin_animal_delete'),
    path('admin-panel/requests/', views.admin_adoption_requests, name='admin_adoption_requests'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/settings/', views.admin_settings, name='admin_settings'),

    # Approve/Reject requests
    path('admin-panel/requests/', views.admin_requests_list, name='admin_requests_list'),
    path('admin-panel/requests/<int:pk>/approve/', views.admin_request_approve, name='admin_request_approve'),
    path('admin-panel/requests/<int:pk>/reject/', views.admin_request_reject, name='admin_request_reject'),
    path("admin-panel/requests/success/<int:animal_id>/", views.request_success, name="request_success"),
    path("admin-panel/requests/rejected/<int:animal_id>/", views.request_rejected, name="request_rejected")
]

