from django.urls import path
from .views import *
app_name = 'accounts'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', UserDeleteView.as_view(), name='delete'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/update/', ProfileUpdateView.as_view(), name='update'),

]