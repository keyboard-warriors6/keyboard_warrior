from django.urls import path
from .views import *
app_name = 'accounts'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='singup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<username>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<username>/update', ProfileUpdateView.as_view(), name='update'),

]