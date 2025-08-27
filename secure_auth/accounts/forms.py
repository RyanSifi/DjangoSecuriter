from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class SecureLoginForm(AuthenticationForm):
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not email or not password:
            raise ValidationError("Email et mot de passe sont requis.")

        try:
            user = self.get_user(email)
        except Exception:
            user = None

        if user:
            if user.account_locked_until and user.account_locked_until > timezone.now():
                raise ValidationError("Ce compte est temporairement verrouillé. Veuillez réessayer plus tard.")

            user_auth = authenticate(request=self.request, username=email, password=password)

            if user_auth is None:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 3:
                    user.account_locked_until = timezone.now() + timedelta(minutes=30)
                user.save()
                raise ValidationError("Email ou mot de passe incorrect.")

            else:
                user.failed_login_attempts = 0
                user.account_locked_until = None
                user.save()
                self.user_cache = user_auth
        else:
            raise ValidationError("Email ou mot de passe incorrect.")

        return self.cleaned_data