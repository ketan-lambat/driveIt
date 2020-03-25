from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    def save(self, commit=True):
        u = super().save(commit=False)
        u.is_active = False
        if commit:
            u.save()
        return u
