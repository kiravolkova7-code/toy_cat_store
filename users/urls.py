
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import RegisterView
from users.forms import EmailAuthenticationForm

app_name = 'users'

urlpatterns = [
    path('login/',
        LoginView.as_view(
            template_name='login.html',
            authentication_form=EmailAuthenticationForm,
        ),
        name='login',
    ),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name='logout'),
    path('register/', RegisterView.as_view(template_name = 'register.html'), name='register'),
]
