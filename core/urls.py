from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .views import (
    FilterWinkel,
    СhooseTypeEvent,
    FilterDayView,
    CalendarView,
    DayView,
    event,
    Sepautoservice,
    
    generate_pdf,
    delete
)
app_name = 'core'

urlpatterns = [
    # post views
    #path('', index, name='index'),
    #path('', user_login, name='login'),
   
   
    path('accounts/profile/', CalendarView.as_view(), name='calendar'),
    
    
    
    path("calendar/", CalendarView.as_view(), name='calendar'),
    
    
    path("calendar/", FilterWinkel.as_view(), name='filterwinkel'),
    
    
    
    
    path('calendar/event/new/', event, name='event_new'),
    
    path('event/delete/<int:event_id>/', delete, name='delete'),
    
    path('', auth_views.LoginView.as_view(template_name="registration/login.html")),
    
    path('calendar/event/edit/<int:event_id>/', event, name='event_edit'),
    
    path('calendar/day/<int:day>/<int:month>/<int:year>/generate_pdf', generate_pdf, name='generate_pdf'),
    
    
    path('calendar/day/edit/<int:day>/<int:month>/<int:year>', DayView.as_view(), name='day'),
    
    path('calendar/day/edit/<int:day>/<int:month>/<int:year>/', DayView.as_view(), name='filterdaywinkel'),
    path('calendar/day/edit/', FilterDayView.as_view(), name='filterdaywinkel'),
    
    path('sepautoservice/', Sepautoservice.as_view() , name='sepautoservice'),
]


