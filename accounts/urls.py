from django.urls import include, path
from .import views

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('<str:username>/', views.user_profile, name = 'user_profile'),
]
