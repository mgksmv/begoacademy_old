from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Gallery, PostImage
from seminars.models import Seminar


def gallery(request):
    gallery_list = Gallery.objects.all().order_by('seminar')

    paginator = Paginator(gallery_list, 12)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    context = {
        'gallery': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }

    return render(request, 'gallery/gallery.html', context)


def gallery_page(request, gallery_url):
    past_seminars = Seminar.objects.filter(is_finished=True)
    one_gallery = Gallery.objects.filter(url=gallery_url)
    photo_list = PostImage.objects.all()

    context = {
        'seminars': past_seminars,
        'gallery': one_gallery,
        'photo_list': photo_list,
    }

    return render(request, 'gallery/gallery_page.html', context)
