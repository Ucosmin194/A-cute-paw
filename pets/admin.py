from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from import_export.admin import ImportExportModelAdmin

from pets.models import *

# admin.site.register(Owner)
# admin.site.register(Pet)
# admin.site.register(Specie)
# admin.site.register(AdoptionRequest)
# admin.site.register(BlogPost)
admin.site.register(Permission)


class BlogPostAdmin(ImportExportModelAdmin):
    pass


admin.site.register(BlogPost, BlogPostAdmin)


class AdoptionRequestAdmin(ImportExportModelAdmin):
    pass


admin.site.register(AdoptionRequest, AdoptionRequestAdmin)


class SpecieAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Specie, SpecieAdmin)


class PetAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Pet, PetAdmin)

# class OwnerAdmin(ImportExportModelAdmin):
#     pass


admin.site.register(Owner, UserAdmin)

# Register your models here.
