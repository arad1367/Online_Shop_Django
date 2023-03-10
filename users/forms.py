from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'focus:outline-none',
                                                                            'placeholder': 'example@gmail.com' }))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'focus:outline-none',
                                                                            'placeholder': 'Your name please' }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'focus:outline-none',
                                                                            'placeholder': 'Make a strong password' }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'focus:outline-none',
                                                                            'placeholder': 'Type password again' }))

    # This is built in user model > collection or table
    class Meta:
        model=User
        fields = ('email', 'username', 'password1', 'password2')

    # Now we need to save the user
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user