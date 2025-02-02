from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializer import RegistrationSuccessSerializer, UserSerializer, RecordSerializer, ChangeRecordSerializer, \
    ChangeClickSerializer, ChangeBalanceSerializer, MessageResponseSerializer, DetailResponseSerializer


# Create your views here.
class RegistrationAPIView(GenericAPIView):
    """
    Регистрация пользователя
    """
    serializer_class = RegistrationSuccessSerializer

    @extend_schema(responses={201: RegistrationSuccessSerializer,
                              400: MessageResponseSerializer})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            data = serializer.data
            data['refresh'] = str(refresh)
            data['access'] = str(access)
            data['message'] = "Вы успешно зарегистрировались"

            return Response(data, status=status.HTTP_201_CREATED)

        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(TokenObtainPairView):
    """ Авторизация пользователя. Т.к. я бог программирования. Я разобрался."""
    @extend_schema(responses={200: TokenObtainPairSerializer,
                              401: DetailResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)

class UserView(GenericAPIView):
    """Получение данных текущего пользователя"""

    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(data=serializer.data)


class UserRecords(GenericAPIView):
    """Получение данных рекордов в обратном порядке"""
    permission_classes = (IsAuthenticated,)
    serializer_class = RecordSerializer

    def get(self, request):
        users = User.objects.order_by('-record')[:10]
        serializer = RecordSerializer(users, many=True)
        return Response(data=serializer.data)

class UpdateBalance(GenericAPIView):
    """Заменить текущее значение баланса пользователя на указавнную сумму"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeBalanceSerializer

    def put(self, request):
        user = request.user
        user.balance = request.data["balance"]
        user.save()
        return Response(data={'message': 'Баланс успешно изменён'})

class UpdateRecord(GenericAPIView):
    """Изменить значение рекорда пользователя"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeRecordSerializer

    def put(self, request):
        user = request.user
        user.record = request.data["record"]
        user.save()
        return Response(data={'message': 'Рекорд успешно изменён'})

class UpdateClicks(GenericAPIView):
    """Изменить число кликов по кроту"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeClickSerializer

    def put(self, request):
        user = request.user
        user.clicks_on_mole = request.data["clicks_on_mole"]
        user.save()
        return Response(data={'message': 'Кол-во кликов по кроту успешно изменено'})