from django.shortcuts import render, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

@login_required
def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['admin_id'] = user.id
                return redirect('home')
            else:
                messages.error(request, "User inactive")
        elif user is None:
            messages.error(request, "Username or password you've entered is incorrect")
    posts = Post.objects.all()
    top_picks = Post.objects.all()[:3]
    paginator = Paginator(posts, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/home.html', {'posts': posts, 'top_picks': top_picks})


@login_required
def post_form(request):
    return render(request, 'blog/post_form.html', context=None)


@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.user
        slug = slugify(title)
        content = request.POST['content']

        if Post.objects.filter(title=title).count() == 0:
            Post.objects.create(title=title, slug=slug, author=author, content=content).publish()
        return redirect('home')
    return redirect('home')


@login_required
def post_edit_form(request):
    if request.method == "POST":
        slug = request.POST['slug']

        post = Post.objects.get(slug=slug)
        return render(request, 'blog/post_edit_form.html', {'post': post})
    return redirect('home')


@login_required
def post_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        slug = request.POST['slug']

        post = Post.objects.get(slug=slug)
        post.title = title
        post.slug = slug
        post.content = content

        post.update()
        return redirect('home')
    return redirect('home')

@login_required
def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_delete(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post_delete.html', {'post': post})


@login_required
def post_delete_confirm(request, slug):
    Post.objects.get(slug=slug).delete()
    return redirect('home')



@login_required
def my_posts(request):
    posts = Post.objects.filter(author = request.user)
    paginator = Paginator(posts, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/my_posts.html', {'posts': posts})
