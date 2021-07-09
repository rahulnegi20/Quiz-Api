from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer, QuizSerializer

from core.models import Quiz
from datetime import timedelta
from django.utils import timezone 
import pytz 
import datetime




def get_current_time():
    today_date = datetime.datetime.now()
    # today_time = datetime.datetime.now().time()
    # print('date=', today_date, today_time)
    # res = today_date  + timedelta(days=1) - timedelta(seconds=1) 
    # print('This is res==',res)
    return today_date



class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class QuizView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes =(permissions.IsAuthenticated,)


today_date = get_current_time()
class PastQuizView(QuizView):
    queryset = Quiz.objects.filter(end_at__lt=today_date,
                     is_published=True)


class LiveQuizView(QuizView):

    #print('Live quiz=', today_date)
    queryset = Quiz.objects.filter(start_at__lte=today_date,
                    end_at__gte=today_date,
                    is_published=True)


class UpcomingQuizView(QuizView):
    queryset = Quiz.objects.filter(start_at__gt=today_date,
                    is_published=True)