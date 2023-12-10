from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import  HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, View, ListView, DetailView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import SignUpForm, CreateAndUpdatePostForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from .models import Rubric, Post, FavoriteUserAnnouncements
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def send_verify_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}')
        message = f'Здравствуйте, {user.username}! Перейдите по ссылке ниже для подтверждения почты:\n\n{verify_url}'
        send_mail('Подтверждение почты', message, 'sayranbekov.0000@gmail.com', [user.email])
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        print(user)
        user.is_active = False
        user.save()
        self.send_verify_email(user)
        return response
    
class VerificationSuccess(TemplateView):
    template_name = 'verification_success.html'

class VerificationError(TemplateView):
    template_name = 'verification_error.html'

class VerifyEmailView(View):
    def get(self, request, user_id, token):
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verify_success')
        else:
            return redirect('verify_error')

class Login(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(password=password,username=username)
        if user is not None and user.is_active:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse_lazy('login')+'?active=false')

class LogOutView(LogoutView):
    next_page = reverse_lazy('login')
        
class HomePageView(LoginRequiredMixin,ListView): # главная страница для просмотра всех рубрик и его подрубрик
    model = Rubric
    template_name = 'home.html'
    context_object_name = 'categories'
    
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        if self.kwargs:
            rubric_pk = self.kwargs['pk']
            subrubrics = Rubric.objects.filter(parent_id = rubric_pk)
        
            context['subcategories'] = subrubrics
        
        return context

class CheckSubRubricDetails(LoginRequiredMixin,DetailView): # для просмотра объявлении подрубрики
    model = Rubric
    template_name = 'subrubric_details.html'
    context_object_name = 'subrubric_posts'
    
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: # добавляем переменную для просмотра кол-во постов
        context = super().get_context_data(**kwargs)
        all_posts = Post.objects.filter(rubric = self.kwargs['pk'])
        
        context['subrubric_posts_counter'] = len(all_posts) # кол-во постов
        context['subrubric_posts'] = all_posts # получить и сохранить отфильтрованные посты
    
        context['liked_posts'] = FavoriteUserAnnouncements.objects.all()
        # передаем туда данные таблицы о лайках пользователей
    
        return context

class SubrubricDetailsView(LoginRequiredMixin,DetailView): # для детального просмотра объявления
    model = Post
    template_name = 'subrubric.html'
    context_object_name = 'post'
    
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk'] # первичный ключ объявления
        subrubric_pk = Post.objects.get(id = post_pk).rubric_id # взял id подрубрики
        
        context['subrubric_detail_id'] = subrubric_pk
        return context

class ViewUsersPosts(LoginRequiredMixin,ListView): # для просмотра объявлении определенного пользователя
    model = Post
    template_name = 'user_profile.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('login')
    
def DeleteUserPost(request,post_pk):
    post = Post.objects.get(id = post_pk)
    post.delete()
    
    return redirect('user-profile', request.user.pk)

class CreateUserPost(LoginRequiredMixin,CreateView): # для создания объявления
    model = Post
    form_class = CreateAndUpdatePostForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class UpdateUserPost(LoginRequiredMixin,UpdateView): # для редактирования объявления
    model = Post
    template_name = 'update_post.html'
    form_class = CreateAndUpdatePostForm
    success_url = reverse_lazy('home')
    
def CheckedUserPost(request,post_pk): # ЛОГИКА ЛАЙКОВ, поставить лайк можно через ' ПОДРОБНЕЕ '
    post = get_object_or_404(Post, id = post_pk) # беру объявление под которым был нажат checkbox
    user = request.user # беру текущего пользователя 
    
    user_announcement = FavoriteUserAnnouncements.objects.filter(user = user, post = post).first()
    
    # если такие данные существуют - удаляем, иначе создаем и сохраняем
    if user_announcement:
        user_announcement.delete()
    else: 
        user_announcement = FavoriteUserAnnouncements.objects.create(user = user, post = post)
        user_announcement.save()

    return redirect('home')

class ViewUserAnnouncements(LoginRequiredMixin,ListView):
    model = FavoriteUserAnnouncements
    template_name = 'user_annoucements.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        x = Post.objects.all()
        queryset = FavoriteUserAnnouncements.objects.all()
        
        result = list()
        for i in range(0,len(queryset),1):
            if x[i].author == queryset[i].user:
                result.append(x[i])
        
        context['posts'] = result
        
        return context