import http
from PIL import Image

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from a_cute_paw.settings import EMAIL_HOST_USER

from pets.filters import *
from pets.forms import *
from pets.models import *


class HomeTemplateView(TemplateView):
    """
    View for home page, has a context of all pets. Inherits from Django's TemplateView
    """
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        return {'all_pets': Pet.objects.all()}


# PET ADD PET, OFFER FOR ADOPT, LIST OF PETS, DETAILS OF PETS


class AdoptionRequestCreateView(LoginRequiredMixin, CreateView):
    """
    Creation view for an adoption request. Inherits from Django's CreateView.
    Can't be accessed without being logged in first -> the inheritance from django's LoginRequiredMixin.
    It sends to the specific template and then return to list of pets page
    """
    template_name = 'pets/adopting_pet.html'
    form_class = AdditionalOwnerForm
    model = AdoptionRequest
    success_url = reverse_lazy('list_pets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pet_id = self.request.GET.get('pet_id')
        context['pet'] = Pet.objects.get(id=pet_id)
        return context

    def get_initial(self):
        print(self.request.GET.get('pet_id'))
        return {'pet': self.request.GET.get('pet_id')}

    def form_valid(self, form):
        """
        Checks whether the info added by the user has the right format for the specified fields
        :param form: the adoption form
        :return: a http response of success_url, otherwise it tells the user the form is invalid
        """
        if form.is_valid() and not form.errors:
            adopt_pet = form.save(commit=False)
            adopt_pet.new_owner = self.request.user
            adopt_pet.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)


class PetCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a pet for adoption.
    Can't be accessed without being logged in first -> the inheritance from django's LoginRequiredMixin.
    It also has a form validity check, and it is linked to the template which contains the data to be filled about
    the pet.
    """
    template_name = 'pets/offer_for_adoption.html'
    form_class = PetForm
    model = Pet
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.is_valid() and not form.errors:
            create_pet: Pet = form.save(commit=False)
            create_pet.owner = self.request.user
            create_pet.save()
            return HttpResponseRedirect(self.success_url)
            #return HttpResponseRedirect(f'{reverse_lazy("crop_image")}?image_path={create_pet.file.url}')
        else:
            return self.form_invalid(form)


class PetListView(ListView):
    """
    A view to show the list of all pets available for adoption. As long as a pet has an 'active=True' status, it will
    appear on the template that's used for this feature.

    """

    template_name = 'pets/list_of_pets.html'
    model = Pet
    context_object_name = 'list_pets'

    def get_queryset(self):
        return Pet.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        data = super(PetListView, self).get_context_data()
        pets = self.get_queryset()
        myFilter = PetFilter(self.request.GET, queryset=pets)
        data = get_paginated_pets(self.request, myFilter.qs, data)
        data['myFilter'] = myFilter

        return data


class PetDetailView(DetailView):
    """
    A details view that is used to show the details of one specific pet that the use selects.
    """
    template_name = 'pets/details_pet.html'
    model = Pet


class AdoptionRequestView(ListView):
    """
    A view that's used to see the adoptions requests. It shows the current adoption requests that are started by a user.
    Will be shown in the user profile and will be split into 'adoption requests to you' and 'adoption requests by you'
    """
    template_name = 'pets/adoption_requests.html'
    model = AdoptionRequest
    context_object_name = 'adopt_requests'

    def get_queryset(self):
        return AdoptionRequest.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        user_pets = Pet.objects.filter(owner=user)
        context['adopt_requests_to_you'] = AdoptionRequest.objects.filter(Q(pet__in=user_pets) &
                                                                          ~(Q(confirmed=True) | Q(confirmed=False)))
        context['adopt_requests_by_you'] = AdoptionRequest.objects.filter(Q(new_owner=user))
        return context


class AdoptionRequestDeleteView(DeleteView):
    """
    View for deleting an adoption request
    """
    template_name = 'pets/adoption_request_delete.html/'
    model = AdoptionRequest

    def get_success_url(self):
        return reverse_lazy('adoption_request')


class PetUpdateView(UpdateView):
    """
    A view that lets a user update a pet
    """
    template_name = 'pets/update_info_pet.html'
    model = Pet
    form_class = PetForm

    def get_success_url(self):
        return reverse_lazy('detail_pet', kwargs={'pk': self.object.id})


class PetDeleteView(DeleteView):
    """
    A view that lets a user delete a pet
    """
    template_name = 'pets/delete_pet.html'
    model = Pet

    def get_success_url(self):
        return reverse_lazy('owner_profile', kwargs={'pk': self.object.owner.id})


# OWNER CREATE USER, USER PROFILE


class OwnerCreateView(CreateView):
    """
    View for creating a user. It has a form validation implemented
    """
    template_name = 'owner/owner_form.html'
    model = Owner
    form_class = OwnerForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if form.is_valid() and not form.errors:
            create_user = form.save(commit=False)
            create_user.username = form.cleaned_data['username']
            create_user.save()
            message = f"Hello {create_user.first_name} {create_user.last_name} \n Welcome to my app! \n Your username is: {create_user.username}"
            send_mail('Create a new user', message, from_email=EMAIL_HOST_USER, recipient_list=[create_user.email])
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)


class OwnerEditProfile(UpdateView):
    """
    View for updating the info on the user
    """
    template_name = 'owner/owner_profile.html'
    model = Owner
    context_object_name = 'owner_profile'
    form_class = OwnerEditForm

    def get_success_url(self):
        return reverse_lazy('owner_profile', kwargs={'pk': self.object.id})


def get_pets(request):
    """

    :param request:
    :return: returns the pets a user has for adoption
    """
    owner_pets = Pet.objects.get(pk=request.GET.get('owner'))
    return owner_pets


# BLOG POSTS
class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View for creating blog articles on different species of pets. Requires special permission to post
    """
    template_name = 'blog/create_post.html'
    model = BlogPost
    form_class = BlogPostForm
    success_url = reverse_lazy('all_posts')
    permission_required = 'pets.add_blogpost'


class BlogListView(ListView):
    """
    View for a list to all the blog articles
    """
    template_name = 'blog/all_posts.html'
    model = BlogPost
    context_object_name = 'blog_posts'

    def get_context_data(self, **kwargs):
        data = super(BlogListView, self).get_context_data()
        post = BlogPost.objects.filter()
        blogFilter = BlogFilter(self.request.GET, queryset=post)
        data['blog_posts'] = blogFilter.qs
        data['blogFilter'] = blogFilter

        return data


class BlogEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View that let's the user with special permissions to uodate a blog article
    """
    template_name = 'blog/edit_post.html'
    model = BlogPost
    context_object_name = 'edit_post'
    form_class = BlogPostForm
    permission_required = 'pets.change_blogpost'

    def get_success_url(self):
        return reverse_lazy('details_post', kwargs={'pk': self.object.id})


class BlogDetailView(DetailView):
    """
    A view that let's you see the details of a blog (full text, author etc)
    """
    template_name = 'blog/post_details.html'
    model = BlogPost


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """"
    A view that allows you to delete a blog post.
    """
    template_name = 'blog/delete_post.html'
    model = BlogPost
    success_url = reverse_lazy('all_posts')
    permission_required = 'pets.delete_blogpost'


# CROPPING IMAGE
# def image_crop_view(request):
#     image_path = request.GET.get('image_path', '/static/image/catblog.jpg')
#     if request.method == 'POST':
#         image_path = request.POST.get('image_path', image_path)
#         image_path = image_path[1:]
#
#         top_left_x = int(float(request.POST.get('top_left_x')))
#         top_left_y = int(float(request.POST.get('top_left_y')))
#         height = int(float(request.POST.get('height')))
#         width = int(float(request.POST.get('width')))
#
#         img = Image.open(image_path)
#         area = (top_left_x, top_left_y, top_left_x + width, top_left_y + height)
#         cropped_img = img.crop(area)
#         cropped_img.save(image_path)
#         return redirect(reverse_lazy('list_pets'))
#
#     return render(request, 'crop_image.html', {'image_path': image_path})


# SWAP BETWEEN OWNERSS
def change_owner(request):
    """

    :param request:
    :return: changes the owner of a pet and sets the active status of a pet when the adoption request is confirmed by
    the user that is the current owner. If it is denied, the owner stay the same and the pet will not be shown for
    adoption anymore.
    """
    # do things...
    if request.method == 'POST':

        adoption_request_id = request.POST['adoption_request_id']
        adoption_request = AdoptionRequest.objects.get(id=adoption_request_id)
        pet = adoption_request.pet
        if 'yes' in request.POST:
            pet.owner = adoption_request.new_owner
            pet.active = False
            adoption_request.confirmed = True
        else:
            adoption_request.confirmed = False
        pet.save()
        adoption_request.save()
    return redirect(request.META['HTTP_REFERER'])


# FAVOURITE PET

def favourite(request):
    """

    :param request:
    :return: the pets that are favored by a user
    """
    pets = Pet.objects.filter(users_favourite=request.user)
    return render(request, 'owner/favourite_pet.html', {'favourite': pets})


@login_required
def add_favourite_pet(request, id):
    """

    :param request:
    :param id: the id the pet that is to be added to favorites by a user
    :return: it tells you whether you added or removed the pet from the favorites
    """
    pet = get_object_or_404(Pet, id=id)
    if pet.users_favourite.filter(id=request.user.id).exists():
        pet.users_favourite.remove(request.user)
        messages.success(request, 'You REMOVED ' + pet.name + ' from favourites.')
    else:
        pet.users_favourite.add(request.user)
        messages.success(request, 'You ADDED ' + pet.name + ' to favourites.')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# PAGINATION
def get_paginated_pets(request, queryset, context=None):
    """

    :param request:
    :param queryset:
    :param context:
    :return: returns 12 pets per page in the pet list view
    """
    if context is None:
        context = {}
    products = list(queryset)
    paginator = Paginator(products, 12)

    page_num = request.GET.get('page', 1)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)

    context['all_pets'] = page
    context['pages'] = paginator.get_elided_page_range(number=page_num, on_ends=1, on_each_side=2)

    return context


# combine 2 forms

def two_form_page_view(request):
    """

    :param request:
    :return: a render of 2 forms in a single template
    """
    form1 = PetForm()
    form2 = OwnerForm()
    return render(request, 'owner/owner_profile.html', {'form1': form1, 'form2': form2})


# def search_results(request):
#     q = request.GET.get('q')
#     queryset = Pet.objects.filter(Q(name__icontains=q) | Q(breed__icontains=q))
#     return render(request, 'pets/list_of_pets.html', {'list_pets': queryset})
