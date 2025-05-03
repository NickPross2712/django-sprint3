from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Category, Post
from .constants import POSTS_PER_PAGE, POST_ORDERING  # Импорт констант


def get_published_posts():
    """Возвращает QuerySet опубликованных постов с оптимизированными запросами."""
    return Post.objects.select_related('category', 'author', 'location').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by(POST_ORDERING)  # Используем константу


def index(request):
    post_list = get_published_posts()[:POSTS_PER_PAGE]  # Используем константу
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(
        get_published_posts(),
        id=id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = get_published_posts().filter(
        category=category
    )

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list
    })
