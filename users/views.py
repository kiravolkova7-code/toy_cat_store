from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistrationForm
from .models import User
from django.core.mail import send_mail


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        print("DEBUG: Форма валидна! Пытаемся сохранить пользователя...")
        response = super().form_valid(form)

        subject = 'Добро пожаловать в ToyCatStore!'
        message =  (f"Здравствуйте!\n\n"
        f"Мы рады видеть вас в магазине ToyCatStore.\n\n"
        f"Ваш email ({self.object.email}) был использован для создания учетной записи.\n"
        f"Если это были вы — просто нажмите кнопку ниже, чтобы войти:\n\n"
        f"{self.request.build_absolute_uri('/users/login/')}\n\n"
        f"---\n"
        f"С уважением,\nКоманда ToyCatStore")

        from_email = 'k1ra-volkova-7xenia@yandex.ru'

        try:
            send_mail(subject, message, from_email, [self.object.email])
        except Exception as e:
            print(f"ERROR: Ошибка отправки письма - {e}")

        return response
