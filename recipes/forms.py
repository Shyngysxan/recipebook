from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    """Кіру формасы (қазақша белгілермен)."""

    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"autofocus": True, "autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Құпиясөз",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": "Логин немесе құпиясөз қате. Қайта тексеріп көріңіз.",
        "inactive": "Бұл аккаунт өшірілген.",
    }


class RegisterForm(UserCreationForm):
    """Тіркелу формасы: логин, email, құпиясөз (2 рет)."""

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email")
        labels = {"username": "Логин"}
        help_texts = {"username": "150 таңбаға дейін: әріп, сан және @/./+/-/_ белгілері."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Құпиясөз"
        self.fields["password2"].label = "Құпиясөзді қайталаңыз"
        self.fields["password2"].help_text = ""
        self.fields["username"].widget.attrs.update({"autofocus": True, "autocomplete": "username"})
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Бұл email-мен аккаунт бұрын тіркелген.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
