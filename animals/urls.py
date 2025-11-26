from .views import shelter_settings

urlpatterns += [
    path('admin-panel/settings/', shelter_settings, name='shelter_settings'),
]
