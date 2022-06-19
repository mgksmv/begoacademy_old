from django.views.generic import ListView, DetailView

from .models import Gallery


class GalleryListView(ListView):
    model = Gallery
    paginate_by = 12
    template_name = 'gallery/gallery.html'

    def get_queryset(self):
        return Gallery.objects.all().order_by('seminar')


class GalleryDetailView(DetailView):
    model = Gallery
    slug_field = 'url'
    slug_url_kwarg = 'url'
    template_name = 'gallery/gallery_page.html'

    def get_queryset(self):
        return Gallery.objects.select_related('seminar') \
            .defer('seminar__content', 'seminar__reserve_photo', 'seminar__date_info', 'seminar__hours', 'seminar__type',
                   'seminar__organizer', 'seminar__place', 'seminar__price', 'seminar__participants',
                   'seminar__additional_info', 'seminar__is_only_for_bego', 'seminar__is_finished',
                   'seminar__is_published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lectors_list = []
        for lector in self.object.seminar.lector.all():
            lectors_list.append(lector.name)
        lectors = ', '.join(lectors_list)

        context['lectors'] = lectors
        return context
