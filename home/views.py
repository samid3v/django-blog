from django.shortcuts import get_object_or_404, redirect, render
from post.models import Category, Comment, Post, UserImage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from post.forms import CommentForm, PostForm, UserRegistrationForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def index(request):
    posts = Post.objects.all()
    latest_posts = Post.objects.all().order_by('-create_date')[:3]
    categories = Category.objects.all()
    pages = Paginator(posts, 10)
    page = request.GET.get('page', 1)

    
    try:
        posters = pages.page(page)
    except PageNotAnInteger:
        posters = pages.page(1)
    except EmptyPage:
        posters = pages.page(pages.num_pages)
    context={
        'posts': posters,
        'latest_posts': latest_posts,
        'categories': categories
    }
    return render(request, 'index.html', context)

def category_view(request, id):
    posts = Post.objects.filter(post_category=id)
    latest_posts = Post.objects.all().order_by('-create_date')[:3]
    categories = Category.objects.all()
    context={
        'posts': posts,
        'latest_posts': latest_posts,
        'categories': categories
    }
    return render(request, 'index.html', context)

def view_post(request, id, slug):
    post = get_object_or_404(Post, pk=id)
    latest_posts = Post.objects.filter(author=post.author).order_by('-create_date')[:6]
    categories = Category.objects.all()
    comments = Comment.objects.filter(post=id)
    # user_image = UserImage.objects.get(user_id=post.author)
    if request.method == "POST":
        back = request.POST.get('url')
        form = CommentForm(request.POST)
        content = request.POST.get('comment') 
        if form.is_valid():
            comment = Comment.objects.create(user = request.user, post = post, comment = content)
            comment.save()
            messages.info(request, "Comment Added successfully!")
            return redirect(back)
    else:
        form = CommentForm()
    context={
        'post': post,
        'latest_posts': latest_posts,
        'categories': categories,
        'form': form,
        'comments': comments
    }
    return render(request, 'view_post.html', context)

def search_post(request):
    if request.method=='POST':
        search = request.POST.get('search')
        posts = Post.objects.filter(post__icontains=search)
        latest_posts = Post.objects.all().order_by('-create_date')[:3]
        categories = Category.objects.all()
        context={
            'posts': posts,
            'latest_posts': latest_posts,
            'categories': categories
        }
        messages.info(request, ":results for "+ search)
        return render(request, 'index.html', context)
    
    return redirect('/')

def post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.info(request, "Post created successfully!")
                return redirect('/') 
        else:
            form = PostForm()
                
    else:
        return redirect('/login') 

   

    return render(request, 'create_post.html', {'form': form})

def update_post(request, id, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Post, pk=id)
        if request.method=='POST':
            form = PostForm(request.POST, instance=instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.info(request, "Post updated successfully!")
                return redirect('/') 
        else:
            form = PostForm(instance=instance)
                
    else:
        return redirect('/login') 

   

    return render(request, 'update.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in")
        return redirect('/') 

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.info(request, "Logged in successfully!")
                return redirect('/')
            else:
                messages.warning(request, "something is wrong")
                return redirect('/login')
        else:
                messages.warning(request, "check your credentials")
                return redirect('/login')

    return render(request, 'login.html')

def register_user(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already registered")
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Account created successfully!")
                return redirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_profile(request, id, slug):
    if request.user.is_authenticated:
        if request.user.id == id:
            posts = Post.objects.filter(author=id)
            context = {
                'posts': posts
            }
            return render(request, 'user_profile.html', context)
        
    messages.info(request, "Login to view Profile")
    return redirect('/')

def delete_post(request, id, slug):
    post = get_object_or_404(Post, pk=id)
    if request.method=='POST':
        url = request.POST.get('url')
        if request.user == post.author:        
            post.delete()
            messages.info(request, "deleted successfully!")
            return redirect(url)
    
        messages.info(request, "Action not authorized!!!")
        return redirect("/")
    return render(request, "delete.html", {'post':post})



def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")