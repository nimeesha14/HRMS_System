from django import forms
from .models import User, UserLeave, Announcement,UserProfile
from datetime import date


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if not user.role:
            user.role = User.Roles.EMPLOYEE
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['department','profile_picture','join_date']

class UserLeaveForm(forms.ModelForm):
    class Meta:
        model = UserLeave
        fields = ['start_date','end_date','reason']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','min':date.today()}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','min':date.today()}),
            'reason': forms.Textarea(attrs={'type':'textarea','class': 'form-control','rows':3,'placeholder':'Enter Reason'}),
        }

class AnnounceForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title','content','announce_date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Title'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter Announcement'
            }),
            'announce_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }