from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.core.paginator import Paginator

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    q = request.GET.get('q')
    if q:
        posts = posts.filter(title__icontains=q)  # Simple search by title
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog_list.html', {'posts': page_obj, 'page_obj': page_obj})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog_detail.html', {'post': post})
