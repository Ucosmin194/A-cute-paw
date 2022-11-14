from pets.models import *


def common_data(request):
    # context to be shown on navbar
    navbar_species = Specie.objects.filter(navbar_promo=True)
    navbar_species_secondary = Specie.objects.filter(navbar_promo=False)
    return {'navbar_species': navbar_species,
            'navbar_species_secondary': navbar_species_secondary}

