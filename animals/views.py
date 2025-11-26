from .models import ShelterSettings
from .forms import ShelterSettingsForm

@admin_required
def shelter_settings(request):
    settings = ShelterSettings.objects.first()

    if not settings:
        settings = ShelterSettings.objects.create()

    form = ShelterSettingsForm(request.POST or None, instance=settings)

    if form.is_valid():
        form.save()
        return render(request, 'adminpanel/settings_saved.html')

    return render(request, 'adminpanel/shelter_settings.html', {'form': form})
