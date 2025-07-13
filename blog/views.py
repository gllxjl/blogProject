from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .services.read_service import ReadService

read_service = ReadService()

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    read_service.increase_read_count(blog_id)

    try:
        count = read_service.cache.get_read_count(blog_id)
        if count is None:
            count = blog.read_count
    except:
        count = blog.read_count

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'read_count': count
    })


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            blog = Blog.objects.create(title=title, content=content)
            return redirect('blog_detail', blog_id=blog.id)
        else:
            return render(request, 'add_blog.html', {'error': '标题和内容不能为空'})
    return render(request, 'add_blog.html')
