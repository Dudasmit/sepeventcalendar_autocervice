import django_filters
from .models import Apointments
                            
class ApointmentsFilter(django_filters.FilterSet):
    
    category = django_filters.ChoiceFilter(choices=Apointments.winkel)
    active = django_filters.BooleanFilter()
    
    

    class Meta:
        model = Apointments
        fields = ['winkel']