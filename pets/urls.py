from django.urls import path
from pets import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    # Owner
    path('offer-for-adoption', views.PetCreateView.as_view(), name='offer_for_adoption'),
    path('owner-form/', views.OwnerCreateView.as_view(), name='owner_form'),
    path('owner-profile/<int:pk>/', views.OwnerEditProfile.as_view(), name='owner_profile'),
    path('adopting-pet/', views.AdoptionRequestCreateView.as_view(), name='adopting_pet'),
    path('adoption-request/', views.AdoptionRequestView.as_view(), name='adoption_request'),
    path('change-owner/', views.change_owner, name='change_owner'),
    path('adoption-request-delete/<int:pk>/', views.AdoptionRequestDeleteView.as_view(), name='adoption_request_delete'),
    # Pet
    path('list-pets/', views.PetListView.as_view(), name='list_pets'),
    path('about-pet/<int:pk>/', views.PetDetailView.as_view(), name='detail_pet'),
    path('favourites/', views.favourite, name='favourite'),
    path('favourites/favourite-pet/<int:id>/', views.add_favourite_pet, name='favourite_pet'),
    path('update-pet/<int:pk>', views.PetUpdateView.as_view(), name='update_pet'),
    path('delete-pet/<int:pk>', views.PetDeleteView.as_view(), name='delete_pet'),
    # Blog
    path('all-posts/', views.BlogListView.as_view(), name='all_posts'),
    path('create-post/', views.BlogCreateView.as_view(), name='create_post'),
    path('details-post/<int:pk>/', views.BlogDetailView.as_view(), name='details_post'),
    path('edit-post/<int:pk>/', views.BlogEditView.as_view(), name='edit_post'),
    path('delete-post/<int:pk>/', views.BlogDeleteView.as_view(), name='delete_post'),
    # jcrop
    # path('crop-image', views.image_crop_view, name='crop_image'),



]
