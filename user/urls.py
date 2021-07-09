from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('all_quiz/', views.QuizView.as_view(), name='all-quiz'),
    path('past/', views.PastQuizView.as_view(), name='past-quiz'),
    path('live/', views.LiveQuizView.as_view(), name='live-quiz'),
    path('upcoming/', views.UpcomingQuizView.as_view(), name='future-quiz'),
]