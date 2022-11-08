from django.shortcuts import render, redirect
from base.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import Post
from .filters import PostFilter

# Create your views here.

def home(request):
    posts = Post.objects.filter(blog=False, active=True, featured=True)[0:3]
    blogposts = Post.objects.filter(blog=True, active=True, featured=True)[0:3]
    context = {'posts': posts, 'blogposts': blogposts}
    return render(request, 'base/index.html', context)

def blogposts(request):
    blogposts = Post.objects.filter(blog=True, active=True)
    myFilter = PostFilter(request.GET, queryset=blogposts)
    posts = myFilter.qs

    page = request.GET.get('page')
    paginator = Paginator(posts, 9)
    
    try:
        blogposts = paginator.page(page)
    except PageNotAnInteger:
        blogposts = paginator.page(1)
    except EmptyPage:
        blogposts = paginator.page(paginator.num_pages)

    context = {'blogposts': blogposts, 'myFilter': myFilter}
    return render(request, 'base/blogposts.html', context)

def posts(request):
    posts = Post.objects.filter(blog=False, active=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs

    page = request.GET.get('page')
    paginator = Paginator(posts, 9)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'myFilter': myFilter}
    return render(request, 'base/posts.html', context)

def post(request, slug):
    post = Post.objects.get(slug=slug)
    context = {'post': post}
    return render(request, 'base/post.html', context)

def profile(request):
    return render(request, 'base/profile.html')

@login_required(login_url="home")
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('posts')
    
    context = {'form': form}
    return render(request, 'base/post_form.html', context)

@login_required(login_url="home")
def updatePost(request, slug):
	post = Post.objects.get(slug=slug)
	form = PostForm(instance=post)

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			form.save()
		return redirect('posts')

	context = {'form':form}
	return render(request, 'base/post_form.html', context)

@login_required(login_url="home")
def deletePost(request, slug):
	post = Post.objects.get(slug=slug)

	if request.method == 'POST':
		post.delete()
		return redirect('posts')
	context = {'item':post}
	return render(request, 'base/delete.html', context)

@csrf_exempt
def sendEmail(request):
    
    if request.method == 'POST':
        
        template = render_to_string('base/email_template.html', {
			'name':request.POST['name'],
			'email':request.POST['email'],
			'message':request.POST['message'],
			})

        email = EmailMessage(
			request.POST['subject'],
			template,
			settings.EMAIL_HOST_USER,
			['pedro.magnomuller@gmail.com']
			)
        
        email.fail_silently=False
        email.send()
    
    return render(request, 'base/email_sent.html')
