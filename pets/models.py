from django.contrib.auth.models import AbstractUser
from django.db import models


class Owner(AbstractUser):
    """
    Model for Owner, inherited from AbstractUser. In addition to the fields inherited from AbstractUser, we added phone
    number, address, city, a photo, plus the extra control fields is_adult and updated_at.
    """
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=100)
    file = models.ImageField(upload_to='static/image/owner_profile', null=True)

    is_adult = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def pets(self):
        return Pet.objects.filter(owner=self)


class Specie(models.Model):
    """
    Model for species, inherits from django default model template.
    """
    name = models.CharField(max_length=100)
    navbar_promo = models.BooleanField(default=False)
    name_plural = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Pet(models.Model):
    """
    Model for pet, inherits from django default model template. Foreign keys on Specie model and on Owner model.
    It has fields about the pet, the repr of the owner, the species they are part from, whether it was added as a
    favorite of a user and also control fields, like if it's active, when it was added or updated.
    """
    size_options = (('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'))
    coat_options = (('short', 'Short'), ('medium', 'Medium'), ('long', 'Long'))
    gender_options = (('male', 'Male'), ('female', 'Female'))

    species = models.ForeignKey(Specie, on_delete=models.CASCADE, null=True, blank=True)
    breed = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30)
    breed_size = models.CharField(max_length=6, choices=size_options, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=gender_options, null=True, blank=True)
    coat_length = models.CharField(max_length=6, choices=coat_options, null=True, blank=True)
    house_trained = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    neutered = models.BooleanField(default=False)
    file = models.ImageField(upload_to='static/image/pets', null=True)
    users_favourite = models.ManyToManyField(Owner, related_name='users_favourite', blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.breed}'


class AdoptionRequest(models.Model):
    """
    The model for the Adoption request, contains foreign keys on Pet model and Owner model(for the new owner to be)
    A series of info about the user that asks to adopt the pet in reference and some control info on the request.
    """
    YES_NO = (('yes', 'Yes'), ('no', 'No'))
    KEEP_OPTIONS = (('house', 'House'), ('garden', 'Garden'), ('crate', 'Crate'), ('other', 'Other'))

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    new_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    family_agrees = models.CharField(max_length=3, choices=YES_NO, default='yes')
    have_children = models.CharField(max_length=3, choices=YES_NO, default='yes')
    any_allergies = models.CharField(max_length=3, choices=YES_NO, default='yes')
    have_pets_now = models.CharField(max_length=3, choices=YES_NO, default='yes')
    had_pets_in_the_past = models.CharField(max_length=3, choices=YES_NO, default='yes')
    reasons_for_adoption = models.TextField(default='')
    place_to_keep = models.CharField(max_length=6, choices=KEEP_OPTIONS, default='house')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(null=True, blank=True)


class BlogPost(models.Model):
    """
    Model for a Blog Post. It has foreign keys on Owner model(as the author) and on Specie model(about which species it
    relates to).
    """
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    article = models.TextField()
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, null=True)
    file = models.ImageField(upload_to='static/image/blog', null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.author}'
