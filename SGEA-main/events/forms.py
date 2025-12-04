from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Event

class EventForm(forms.ModelForm):
    organizer = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='professor'),
        label='Professor Responsável',
        empty_label='Selecione um professor',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Event
        fields = ['title','event_type','start_date','end_date','time','place','capacity','banner','organizer']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control date-mask', 'placeholder': 'dd/mm/aaaa'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control date-mask', 'placeholder': 'dd/mm/aaaa'}),
            'time': forms.TextInput(attrs={'class': 'form-control time-mask', 'placeholder': '00:00'}),
            'banner': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError('A data de início não pode ser anterior à data atual.')
        return start_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('A data de término não pode ser anterior à data de início.')
        
        return cleaned_data

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None and capacity <= 0:
            raise forms.ValidationError('A capacidade deve ser um número positivo.')
        return capacity

    def clean_banner(self):
        banner = self.cleaned_data.get('banner')
        if banner:
            if not banner.content_type.startswith('image/'):
                raise forms.ValidationError('O arquivo deve ser uma imagem.')
        return banner

