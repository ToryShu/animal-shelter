from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

class Animal(models.Model):
    SPECIES_CHOICES = [
        ('cat', 'Cat'),
        ('dog', 'Dog'),
    ]
    
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    age = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='animals/', blank=True, null=True)
    adopted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.species})"

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='adoption_requests')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request {self.id} - {self.animal.name} by {self.user.username}"


@receiver(post_save, sender=AdoptionRequest)
def update_animal_and_requests(sender, instance, **kwargs):
    if instance.status == 'approved':
        animal = instance.animal
        animal.adopted = True
        animal.save()
        other_requests = AdoptionRequest.objects.filter(animal=animal).exclude(id=instance.id)
        other_requests.update(status='rejected')
