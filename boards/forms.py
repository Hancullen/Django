from django import forms
from .models import Topic

#a model form associated with the Topic model
class NewTopicForm(forms.ModelForm): 
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = Topic

        '''
        'subject' refers to the subject field in Topic class
        define extra field 'message'
        which refers to the message in Post
        '''
        fields = ['subject', 'message'] 
        
