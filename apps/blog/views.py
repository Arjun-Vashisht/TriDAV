from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import BlogPost, BlogCategory


def blog_list(request):
    posts = BlogPost.objects.filter(status='published', published_at__lte=timezone.now())
    category_slug = request.GET.get('category')
    active_category = None

    if category_slug:
        active_category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=active_category)

    paginator = Paginator(posts, 9)
    page = paginator.get_page(request.GET.get('page', 1))

    context = {
        'posts': page,
        'categories': BlogCategory.objects.all(),
        'active_category': active_category,
        'featured_post': BlogPost.objects.filter(status='published', is_featured=True).first(),
        'meta_title': 'Textile Orders Blog – TriDAV Impex',
        'meta_description': 'Expert guides on home textiles, hotel bedding, thread count, GSM, and buying tips for B2B buyers.',
    }
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    post.views += 1
    post.save(update_fields=['views'])

    related = BlogPost.objects.filter(
        status='published', category=post.category
    ).exclude(pk=post.pk)[:3]

    context = {
        'post': post,
        'related': related,
        'meta_title': post.effective_seo_title,
        'meta_description': post.effective_seo_description,
        'og_image': post.og_image or post.featured_image,
        'schema_article': True,
    }
    return render(request, 'blog/detail.html', context)
