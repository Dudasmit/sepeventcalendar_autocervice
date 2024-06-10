from django import forms
from django.forms import ModelForm, DateInput
from core.models import Apointments



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    

class EventForm(ModelForm):
  class Meta:
    model = Apointments
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'date', 'width':'5000px'}, format='%Y-%m-%d'),
      #'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    exclude = ["user"]#,"typeevent","winkel"]
    fields = '__all__'
    

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%d',)
    
    
    
    #self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    
class DayForm(ModelForm):
  class Meta:
    model = Apointments
    fields = '__all__'
