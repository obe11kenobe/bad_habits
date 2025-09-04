from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated] # только авторизация
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title"]

    def get_queryset(self):
        # показываем только привычки текущего юзера
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # автоматически проставляем владельца
        serializer.save(user=self.request.user)