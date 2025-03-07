from django.shortcuts import reverse
from django.views.generic import TemplateView, CreateView, ListView
from django.core.paginator import Paginator

from core.models import Master, Service, Visit, Review
from core.forms import VisitForm, ReviewForm

MENU = [
    {'title': 'Главная', 'url': '/', 'active': True},
    {'title': 'Мастера', 'url': '/#masters', 'active': True},
    {'title': 'Услуги', 'url': '/#services', 'active': True},
    {'title': 'Запись на стрижку', 'url': '/#orderForm', 'active': True},
    {'title': 'Отзывы', 'url': '/#reviews', 'active': True},
    {'title': 'Оставить отзыв', 'url': '/review', 'active': True},
]


class MainPageView(CreateView):
    template_name = 'main.html'
    form_class = VisitForm
    model = Visit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = MENU
        context['masters'] = Master.objects.all()
        context['services'] = Service.objects.all()

        reviews_objects = Review.objects.filter(status=1).order_by("-rating", "-created_at")

        paginator = Paginator(reviews_objects, 3)
        page_number = self.request.GET.get("page", 1)
        reviews = paginator.get_page(page_number)

        context['reviews'] = reviews

        return context

    def get_success_url(self):
        self.request.session['thanks_message'] = 'Спасибо за заявку! Скоро с вами свяжутся.'
        return reverse("thanks")


class ThanksView(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = MENU
        context['thanks_message'] = self.request.session.pop('thanks_message',
                                                             'Спасибо за посещение сайта Барбершопа!')
        return context


class ReviewView(CreateView):
    template_name = "review.html"
    form_class = ReviewForm
    extra_context = {"menu": MENU}

    def get_success_url(self):
        self.request.session['thanks_message'] = 'Спасибо за отзыв!'
        return reverse("thanks")
