from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Post, Category, Tag, Comment


def home(request):
    posts = Post.objects.select_related('category').prefetch_related('tags').all()
    featured = posts.filter(featured=True).first()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # Search
    query = request.GET.get('q', '')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__icontains=query)
        )

    # Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    # Filter by tag
    tag_slug = request.GET.get('tag', '')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    return render(request, 'home.html', {
        'posts': posts,
        'featured': featured,
        'categories': categories,
        'tags': tags,
        'query': query,
        'active_category': category_slug,
        'active_tag': tag_slug,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)
    related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)[:3]

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        body = request.POST.get('body', '').strip()
        if name and email and body:
            Comment.objects.create(post=post, name=name, email=email, body=body)
            return redirect('post_detail', slug=slug)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    submitted = False
    if request.method == 'POST':
        submitted = True
    return render(request, 'contact.html', {'submitted': submitted})


def author_profile(request, author_name):
    posts = Post.objects.filter(author__iexact=author_name)
    return render(request, 'author.html', {
        'author_name': author_name,
        'posts': posts,
        'post_count': posts.count(),
        'bio': posts.first().author_bio if posts.exists() else '',
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'posts': posts})
