from django.contrib import admin
from django.db.models import Sum

from core.models import Master, Service, Visit, Review


def make_accepted(modeladmin, request, queryset):
    updated = queryset.update(status=1)


def make_cancelled(modeladmin, request, queryset):
    updated = queryset.update(status=2)


def make_completed(modeladmin, request, queryset):
    updated = queryset.update(status=3)


def make_unverified(modeladmin, request, queryset):
    updated = queryset.update(status=0)


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone")
    filter_horizontal = ("services",)
    search_fields = ("first_name", "last_name")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")
    search_fields = ("name", "description")
    list_display_links = ("name", "price")


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):

    def get_total_price(self, obj):
        total = obj.services.aggregate(total=Sum("price"))["total"]
        if total:
            return f"{total:.2f} ₽"
        return "0.00 ₽"

    get_total_price.short_description = "Общая сумма"
    get_total_price.admin_order_field = "services__price"

    make_accepted.short_description = "Подтвердить выбранные записи"
    make_cancelled.short_description = "Отменить записи"
    make_completed.short_description = "Отметить выполненными"
    make_unverified.short_description = "Отметить неподтвержденными"

    list_display = ("name", "phone", "comment", "status", "master", "get_total_price",)
    list_display_links = ("name",)
    list_editable = ("status",)
    search_fields = ("phone", "name", "comment", "services__name")
    ordering = ("master", "status", "created_at")
    list_filter = ("master", "created_at", "status")
    actions = [make_accepted, make_cancelled, make_completed, make_unverified]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "text", "rating", "status", "master")
    list_display_links = ("name",)
    list_editable = ("status",)
    search_fields = ("name", "status", "master", "rating")
    ordering = ("master", "status", "created_at")
    list_filter = ("master", "status", "created_at")

    make_accepted.short_description = "Одобрить выбранные отзывы"
    make_cancelled.short_description = "Отклонить выбранные отзывы"
    make_unverified.short_description = "Отметить не проверенными"

    actions = [make_accepted, make_cancelled, make_unverified]
