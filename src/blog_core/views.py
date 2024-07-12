from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponse

from .forms import RegisterForm, LoginForm, PostForm, ImageForm
from .models import Post, Image, Comment


def index(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return render(request, 'blog_core/index.html', context= {'posts': posts})
    if request.method == 'POST':
        post = Post.objects.get(id=request.POST.get('pk'))
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('memes')
    

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    images = post.images.all()
    comments = post.comments.all()
    return render(request, 'blog_core/post_detail.html', {'post': post, 
                                                          'images': images, 
                                                          'comments': comments})

def add_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if post_form.is_valid() and image_form.is_valid():
            title = post_form.cleaned_data['title']
            body = post_form.cleaned_data['body']
            
            new_post = Post.objects.create(author=request.user,
                                           title=title, 
                                           body=body)
            for img in images:
                Image.objects.create(post=new_post, 
                                     image=img, 
                                     author=request.user)
            return redirect('memes')
    post_form = PostForm()
    image_form = ImageForm()
    context = {'post_form': post_form, 'image_form': image_form}
    return render(request, 'blog_core/add_post.html', context)
        
def delete_post(request: HttpResponse):
    print('hoho')
    if request.method == 'POST':
        print('hoho')
        post = get_object_or_404(Post, id=request.POST['pk'])
        post.delete()
        return redirect('memes')
    
def change_post(request):
    # need to prepolutate form
    id=request.POST['pk']
    post = Post.objects.get(id=id)

    images = post.images.all()
    initial_post_data = {
            'title': 'Default Title',
            'content': 'Default Content',
        }
    post_form = PostForm(initial=initial_post_data)
    # AttributeError at /memes/posts/change/
    # 'ellipsis' object has no attribute '_meta'
    print(post_form.is_bound)
    image_form = ImageForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
    return render(request, 'blog_core/change_post.html', {'post_form': post_form,
                                                          'image_form': image_form})

@login_required(login_url='login')
def account(request):
    return render(request, 'blog_core/account.html');

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'blog_core/register.html', {'form': form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully')
            login(request, user)
            return redirect('account')
        else:
            return render(request, 'blog_core/register.html', {'form': form})

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('memes')
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'blog_core/login.html', {'form': form})
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
                messages.success(request, 'You have signed in successfully')
                return redirect('account')

        messages.error(request, 'This user doesn\'t exist or data are invalid')
        return render(request, 'blog_core/login.html', {'form': form})
    
def sign_out(request):
    logout(request)
    messages.error(request, 'You have been logged out')
    return redirect('memes')
