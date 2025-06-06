from django.db import models
from django.contrib.auth.models import User


class Advertisement(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Открыто'),
        ('CLOSED', 'Закрыто'),
        ('DRAFT', 'Черновик'),
    ]

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # связь с пользователем
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements')

    def __str__(self):
        return f"{self.title} | {self.status}"
