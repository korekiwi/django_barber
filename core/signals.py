import asyncio
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from core.models import Visit
from core.telegram_bot import send_telegram_message
from barber.settings import TELEGRAM_BOT_TOKEN, PERSONAL_CHAT_ID


@receiver(m2m_changed, sender=Visit.services.through)
def send_telegram_notification(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Visit.
    Он обрабатывает добавление КАЖДОЙ услуги в запись на консультацию.
    Отправка ОДНОГО сообщения в телеграмм выполняется в первом условии
    http://127.0.0.1:8000/admin/core/visit/5/change/
    """
    if action == 'post_add' and kwargs.get('pk_set'):
        services = [service.name for service in instance.services.all()]
        # print(f"УСЛУГИ: {services}")
        message = f"""
*Новая запись на консультацию*

*Имя:* {instance.name}
*Телефон:* {instance.phone or 'не указан'}
*Комментарий:* {instance.comment or 'не указан'}
*Услуги:* {', '.join(services) or 'не указаны'}
*Дата создания:* {instance.created_at}
*Мастер:* {instance.master.first_name} {instance.master.last_name}
-------------------------------------------------------------
"""
        asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, PERSONAL_CHAT_ID, message))



