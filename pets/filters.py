import django_filters
from django import forms
from django_filters import CharFilter

from pets.models import Pet, BlogPost


class PetFilter(django_filters.FilterSet):
    """
    Filter for different pets.
    -> Breed and name can be filtered with icontains for it to only contains what the user searched for
    """
    breed_icontains = CharFilter(field_name='breed', lookup_expr='icontains', label='Pet breed',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Search for a breed'}))
    name_icontains = CharFilter(field_name='name', lookup_expr='icontains', label='Pet name',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Name of the pet'}))

    class Meta:
        model = Pet
        fields = ['species', 'breed_icontains', 'breed_size', 'name_icontains', 'age', 'gender', 'coat_length',
                  'house_trained', 'neutered']

    def __init__(self, *args, **kwargs):
        super(PetFilter, self).__init__(*args, **kwargs)

        self.filters['species'].field.widget.attrs.update(
            {'class': 'form-select'})
        self.filters['breed_size'].field.widget.attrs.update(
            {'class': 'form-select'})
        self.filters['age'].field.widget.attrs.update(
            {'class': 'form-control'})
        self.filters['gender'].field.widget.attrs.update(
            {'class': 'form-select'})
        self.filters['coat_length'].field.widget.attrs.update(
            {'class': 'form-select'})
        self.filters['house_trained'].field.widget.attrs.update(
            {'class': 'form-select'})
        self.filters['neutered'].field.widget.attrs.update(
            {'class': 'form-select'})


class BlogFilter(django_filters.FilterSet):
    """
    Filters blogs on species they refer to.
    """
    class Meta:
        model = BlogPost
        fields = ['specie']

    def __init__(self, *args, **kwargs):
        super(BlogFilter, self).__init__(*args, **kwargs)

        self.filters['specie'].field.widget.attrs.update(
            {'class': 'form-select'})
