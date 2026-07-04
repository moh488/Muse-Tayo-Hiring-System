from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import SystemUser


class SystemUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(choices=SystemUser.ROLE_CHOICES, initial='RECRUITER')

    class Meta:
        model = SystemUser
        fields = ('username', 'email', 'phone_number', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number')
        user.is_verified = False
        if commit:
            user.save()
        return user


class SystemUserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SystemUser
        fields = ('username', 'email', 'phone_number', 'role', 'password', 'is_verified', 'is_active')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
