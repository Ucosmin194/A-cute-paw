from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, Select, Textarea, EmailInput
from pets.models import *


class PetForm(forms.ModelForm):
    """
    Form for Pets model, what it should contain and in what forms should the info be asked from the given model
    """
    class Meta:
        model = Pet
        fields = ['species', 'breed', 'breed_size', 'coat_length', 'house_trained', 'neutered', 'name', 'age', 'gender',
                  'description', 'file', 'owner']

        widgets = {
            'owner': forms.HiddenInput(),
            'species': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.TextInput(attrs={'placeholder': 'Please enter the breed', 'class': 'form-control'}),
            'breed_size': forms.Select(attrs={'class': 'form-select'}),
            'coat_length': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'placeholder': 'Please enter the name of the pet', 'class': 'form-control'}),
            'age': forms.NumberInput(
                attrs={'placeholder': 'Please enter the age of the pet', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Please say something about the pet', 'class': 'form-control'}),

        }


class OwnerForm(UserCreationForm):
    """
    Form for Owner model what it should contain and in what forms should the info be asked from the given model
    """
    class Meta:
        model = Owner
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'address',
                  'city', 'file', 'is_adult']

        widgets = {
            'username': TextInput(attrs={'placeholder': 'Please enter an username', 'class': 'form-control'}),
            'first_name': TextInput(attrs={'placeholder': 'Please enter your first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Please enter your last name', 'class': 'form-control'}),
            'email': EmailInput(attrs={'placeholder': 'Please enter your email', 'class': 'form-control'}),
            'phone_number': TextInput(attrs={'placeholder': 'Please enter you phone number', 'class': 'form-control'}),
            'address': TextInput(attrs={'placeholder': 'Please enter your address', 'class': 'form-control'}),
            'city': TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Please enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Please enter your password confirmation'


class AdditionalOwnerForm(forms.ModelForm):
    """
    Form for adopting a pet, what it should contain and in what forms should the info be asked from the given model
    """
    class Meta:
        model = AdoptionRequest

        fields = ['family_agrees', 'have_children', 'any_allergies', 'have_pets_now', 'had_pets_in_the_past',
                  'place_to_keep', 'reasons_for_adoption', 'pet']

        widgets = {
            'pet': forms.HiddenInput(),
            'family_agrees': Select(attrs={'class': 'form-select'}),
            'have_children': Select(attrs={'class': 'form-select'}),
            'any_allergies': Select(attrs={'class': 'form-select'}),
            'have_pets_now': Select(attrs={'class': 'form-select'}),
            'had_pets_in_the_past': Select(attrs={'class': 'form-select'}),
            'reasons_for_adoption': Textarea(
                attrs={'placeholder': 'Please say something about the pet', 'class': 'form-control'}),
            'place_to_keep': Select(attrs={'class': 'form-select'}),

        }


class OwnerEditForm(forms.ModelForm):
    """
    Form for editing the Owner model, what it should contain and in what forms should the info be asked from
    the given model.
    """
    class Meta:
        model = Owner

        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address',
                  'city', 'file']

        widgets = {
            'username': TextInput(attrs={'placeholder': 'Please enter an username', 'class': 'form-control'}),
            'first_name': TextInput(attrs={'placeholder': 'Please enter your first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Please enter your last name', 'class': 'form-control'}),
            'email': EmailInput(attrs={'placeholder': 'Please enter your email', 'class': 'form-control'}),
            'phone_number': TextInput(attrs={'placeholder': 'Please enter you phone number', 'class': 'form-control'}),
            'city': TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
            'address': TextInput(attrs={'placeholder': 'Please enter your address', 'class': 'form-control'}),
        }


class BlogPostForm(forms.ModelForm):
    """
    Form for Blog model, what it should contain and in what forms should the info be asked from the given model
    """
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'article', 'specie', 'file']
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Please enter the post title', 'class': 'form-control'}),
            'author': Select(attrs={'class': 'form-select'}),
            'article': Textarea(attrs={'placeholder': 'Please enter the post content', 'class': 'form-control'}),
            'specie': Select(attrs={'class': 'form-select'}),
        }
