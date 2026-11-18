from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import MeSerializer, RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/drf/auth/register/ – ашық эндпоинт; жауапта құпиясөз қайтарылмайды."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class MeView(generics.RetrieveAPIView):
    """GET /api/drf/auth/me/ – ағымдағы қолданушының профилі (аутентификация керек)."""
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
