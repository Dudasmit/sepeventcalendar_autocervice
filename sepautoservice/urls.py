from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core.views import CalendarView
from .views import (
    FilterDayView,
    Service_CalendarView,
    DayView,
    event,
    
    
    generate_pdf,
    delete
)
app_name = 'sepautoservice'

urlpatterns = [
    # post views
    #path('', index, name='index'),
    #path('', user_login, name='login'),
   
   
    
    
    
    path("sepautoservice/", Service_CalendarView.as_view(), name='calendar'),
    
    
    
    
    
    
    path('sepautoservice/event/new/', event, name='event_new'),
    
    path('sepautoservice/delete/<int:event_id>/', delete, name='delete'),
    
    path('', auth_views.LoginView.as_view(template_name="registration/login.html")),
    
    path('sepautoservice/event/edit/<int:event_id>/', event, name='event_edit'),
    
    path('sepautoservice/day/<int:day>/<int:month>/<int:year>/generate_pdf', generate_pdf, name='generate_pdf'),
    
    
    path('sepautoservice/day/edit/<int:day>/<int:month>/<int:year>', DayView.as_view(), name='day'),
    
    path('sepautoservice/day/edit/<int:day>/<int:month>/<int:year>/', DayView.as_view(), name='filterdaywinkel'),
    path('sepautoservice/day/edit/', FilterDayView.as_view(), name='filterdaywinkel'),
    
    path('calendar/', CalendarView.as_view() , name='levering'),
]


