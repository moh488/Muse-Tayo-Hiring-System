from django import forms
from messages.models import DirectMessage


class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your message...'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject (optional)'}),
        }
