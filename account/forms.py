from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', help_text="A good name for your account.",
                               widget=forms.TextInput(
                                   attrs={'id': 'username', 'placeholder': 'Please Enter your username'}))
    password = forms.CharField(max_length=50, label='Password', help_text="A strong password.",
                               widget=forms.PasswordInput(
                                   attrs={'id': 'password', 'placeholder': 'Please Enter your password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not User.objects.filter(username=username).exists():
            raise ValidationError('Username or password is wrong', code='invalid_username')

        user = User.objects.get(username=username)

        if not user.check_password(password):
            raise ValidationError('Username or password is wrong', code='invalid_password')


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='First Name', help_text="Your first name.",
                                 widget=forms.TextInput(
                                     attrs={'id': 'firstname', 'placeholder': 'Please Enter your first name'}))
    last_name = forms.CharField(max_length=50, label='Last Name', help_text="Your last name.", widget=forms.TextInput(
        attrs={'id': 'lastname', 'placeholder': 'Please Enter your last name'}))
    username = forms.CharField(max_length=50, label='Username', help_text="A good name for your account.",
                               widget=forms.TextInput(
                                   attrs={'id': 'username', 'placeholder': 'Please Enter your username'}))
    email = forms.EmailField(max_length=50, label='Email', help_text="Your email address",
                             widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Please Enter your email'}))
    password1 = forms.CharField(max_length=50, label='Password', help_text="A strong password.",
                                widget=forms.PasswordInput(
                                    attrs={'id': 'password', 'placeholder': 'Please Enter your password'}))
    password2 = forms.CharField(max_length=50, label='Password confirmation', help_text="Confirm your password.",
                                widget=forms.PasswordInput(
                                    attrs={'id': 'password2', 'placeholder': 'Please confirm your password'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if password1 != password2:
            raise ValidationError('Passwords must match', code='invalid_password')
        elif len(password1) < 10:
            raise ValidationError('Password must be at least 10 characters', code='invalid_password_length')
        elif not any(char.isdigit() for char in password1):
            raise ValidationError('Password must contain at least one digit', code='invalid_password_char')
        elif not any(char.isalpha() for char in password1):
            raise ValidationError('Password must contain at least one letter', code='invalid_password_alpha')
        elif not any(char.isupper() for char in password1):
            raise ValidationError('Password must contain at least one uppercase letter', code='invalid_password_upper')
        elif not any(char.islower() for char in password1):
            raise ValidationError('Password must contain at least one lowercase letter', code='invalid_password_lower')
        elif not any(char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')'] for char in password1):
            raise ValidationError('Password must contain at least one special character',
                                  code='invalid_password_special')
        elif User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists', code='invalid_email')
        elif User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists', code='invalid_username')


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={'class': 'input-group form-control py-9 mb-1'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'username': 'Username',
            'image': 'Change Profile Picture'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if self.user and hasattr(self.user, 'profile'):
            self.fields['image'].initial = self.user.profile.image

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        user_id = self.instance.id

        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError('Email already exists', code='invalid_email')
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            raise ValidationError('Username already exists', code='invalid_username')

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('The image size must not exceed 5MB.')
        return image

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        if 'image' in self.cleaned_data and self.cleaned_data['image']:
            user.profile.image = self.cleaned_data['image']
        else:
            user.profile.image = user.profile.image

        if commit:
            user.save()
            user.profile.save()

        return user
