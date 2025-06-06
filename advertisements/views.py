from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешено читать всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменять — только автору
        return obj.creator == request.user

class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


    filterset_class = AdvertisementFilter

    def validate(self, data):
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            open_ads = Advertisement.objects.filter(creator=user, status='OPEN').count()
            if open_ads >= 10:
                raise serializers.ValidationError("Вы не можете иметь больше 10 открытых объявлений.")
        return data

    def get_permissions(self):
        """Определяем права доступа в зависимости от метода запроса."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        """Ограничение: не более 10 открытых объявлений на пользователя."""
        user = self.request.user
        open_ads = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if open_ads >= 10:
            raise PermissionDenied("У вас уже 10 открытых объявлений.")
        serializer.save(creator=user)

    def perform_destroy(self, instance):
        """Удалить объявление может только его автор."""
        if instance.creator != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужое объявление.")
        instance.delete()

    def perform_update(self, serializer):
        """Редактировать объявление может только его автор."""
        if self.get_object().creator != self.request.user:
            raise PermissionDenied("Вы не можете редактировать чужое объявление.")
        serializer.save()

