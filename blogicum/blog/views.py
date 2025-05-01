from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category


def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]  # Переименовано в post_list

    # Исправлено имя переменной
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    try:
        post = Post.objects.get(
            id=id,
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    except Post.DoesNotExist:
        raise Http404(f"Пост с id={id} не найден или недоступен.")

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    try:
        category = Category.objects.get(
            slug=category_slug,
            is_published=True
        )
    except Category.DoesNotExist:
        raise Http404(f"Категория {category_slug} не найдена или недоступна.")

    post_list = Post.objects.filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True
    ).order_by('-pub_date')

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list  # Также исправлено для единообразия
    })
