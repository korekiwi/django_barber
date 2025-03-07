from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views


urlpatterns = (
    [
        path("", views.MainPageView.as_view(), name="main"),
        path("admin/", admin.site.urls),
        path("thanks/", views.ThanksView.as_view(), name="thanks"),
        path("review/", views.ReviewView.as_view(), name="review"),
        # path("some_page", views.some_page, name="some_page"),
        # path("some_page/", views.SomePage.as_view(), name="some_page"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)