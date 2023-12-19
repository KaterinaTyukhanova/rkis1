from django.urls import path
from . import views
from .views import LoginServerView, LogoutServerView

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/change/', views.ChangeQuestionView.as_view(), name='question-change'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', LoginServerView.as_view(), name='login'),
    path('accounts/logout/', LogoutServerView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change/<int:pk>/', views.ChangeUserView.as_view(), name='profile-change'),
    path('profile/delete/<int:pk>/', views.DeleteUserView.as_view(), name='profile-delete'),
]