from django.shortcuts import reverse
from django.views.generic import TemplateView, CreateView, ListView
from django.db.models import Q

from core.models import Master, Service, Visit
from core.forms import VisitForm, ReviewForm

MENU = [
    {'title': 'Главная', 'url': '/', 'active': True},
    {'title': 'Мастера', 'url': '#masters', 'active': True},
    {'title': 'Услуги', 'url': '#services', 'active': True},
    {'title': 'Запись на стрижку', 'url': '#orderForm', 'active': True},
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
        return context

    def get_success_url(self):
        self.request.session['thanks_message'] = 'Спасибо за заявку! Скоро с вами свяжутся.'
        return reverse("thanks")


class ThanksView(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = MENU
        context['thanks_message'] = self.request.session.pop('thanks_message', 'Спасибо за посещение сайта Барбершопа!')
        return context


class ReviewView(CreateView):
    template_name = "review.html"
    form_class = ReviewForm
    extra_context = {"menu": MENU}

    def get_success_url(self):
        self.request.session['thanks_message'] = 'Спасибо за отзыв!'
        return reverse("thanks")
