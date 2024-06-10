

# Create your views here.

from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
from django.shortcuts import redirect
import calendar
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .utils import Calendar,Day
from .forms import EventForm, DayForm
from django.db.models import Q

from io import BytesIO
from reportlab.lib.enums import TA_RIGHT,TA_CENTER 
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import Table,Paragraph, TableStyle, SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import math


pdfmetrics.registerFont(TTFont('Arial', settings.STATIC_ROOT + '/fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', settings.STATIC_ROOT + '/fonts/arialbd.ttf'))


def index(request):
    return HttpResponse('hello')

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("http://localhost:8000/calendar/")#HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    
    


class Service_CalendarView(LoginRequiredMixin, generic.ListView):
    
    model = Service_Apointments
    template_name = 'sepautoservice/calendar.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated == True:
            # Try to dispatch to the right method; if a method doesn't exist,
            # defer to the error handler. Also defer to the error handler if the
            # request method isn't on the approved list.
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect("http://localhost:8000/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        #print(self.request.GET.getlist("typeevent"))
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['filterwinkelname'] = 'filterwinkel'

        
        #context['typeevents'] = WinkelType.get_type_event(self)
        
        return context


    
def filterwinkel(request, winkel=None):
    #login_url = "accounts:signin"
   

    
    apointments = Apointments.objects.filter(
              Q(typeevent__in = winkel)
            )   
                            
    return render(request, CalendarView())
    
    



def prev_day(d):
    first = d
    prev_day = first - timedelta(days=1)

    day_ = '/calendar/day/edit/' + str(prev_day.day) + '/' +  str(prev_day.month) + '/' + str(prev_day.year)
    return day_

def next_day(d):
    last = d
    next_day = last + timedelta(days=1)
    day_ = '/calendar/day/edit/' + str(next_day.day) + '/' +  str(next_day.month) + '/' + str(next_day.year)
    return day_


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month




def event(request, event_id=None):
    if request.user.is_authenticated == False:
        return redirect("http://localhost:8000/")
    
    instance = Service_Apointments()
    delete_url = ''
    if event_id:
        instance = get_object_or_404(Service_Apointments, pk=event_id)
        
        delete_url = Service_Apointments.get_delete_url(instance)
    else:
        instance = Service_Apointments()
        instance.user = request.user
        
        #print(Winkel.objects.filter(winkel__in=request.GET.getlist("winkel")))
        #instance.winkel = get_object_or_404(Winkel, id=request.GET.getlist("winkel")) 
        #instance.typeevent =  get_object_or_404(TypeEvent, id=request.GET.getlist("typeevent")) 
        
    
    
    form = EventForm(request.POST or None, instance=instance)
    
    
    
    if request.POST and form.is_valid():
        #data = request.POST.copy()
        #data.update({'user':request.user.id})
        #form = EventForm(data)
        
        if form.is_valid():
            #form.user= request.user
            form.save()
            return HttpResponseRedirect(reverse('sepautoservice:calendar'))
    
    if request.method == 'delete':
        
        person_obj = Apointments.objects.get(pk=event_id)
        #print(person_obj)
        person_obj.delete()
        return HttpResponseRedirect(reverse('sepautoservice:calendar'))
        

    
    return render(request, 'sepautoservice/event.html', {'form': form, 'get_delete_url':delete_url})


def delete(request, event_id=None):
    if request.user.is_authenticated == False:
        return redirect("http://localhost:8000/")
    Event_ = Apointments.objects.get(pk=event_id)
    
    Event_.delete()
    return HttpResponseRedirect(reverse('sepautoservice:calendar'))

def date_edit(request, day = None, month = None, year = None):
   
    instance = Apointments()
    date_ = day+month+year
    #print(date_[3:7])
    if day:
        instance = get_list_or_404(Service_Apointments, start_time__day=date_[0:2], start_time__month=date_[2:3], start_time__year=date_[3:7]) 
        #instance = get_list_or_404(Apointments, start_time__day=day, start_time__month=month, start_time__year=year) 
    else:
        instance = Apointments()
        
    
    #print(instance)
    #form = DayForm(instance=instance)
    model = Apointments
    template_name = 'sepautoservice/day.html'

    
    

    return render(request, 'sepautoservice/day.html', {'instance': instance, 'date_':date_})



class DayView(generic.ListView):
    
    model = Service_Apointments
    template_name = 'sepautoservice/day.html'
   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated == True:
            # Try to dispatch to the right method; if a method doesn't exist,
            # defer to the error handler. Also defer to the error handler if the
            # request method isn't on the approved list.
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)
        else:
            return redirect("http://localhost:8000/")

    def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs)
        #print('DayView',self.request.GET.getlist("typeevent") ,self.request.GET.getlist("winkel") )
        # use today's date for the calendar
        d = datetime(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'])

        # Instantiate our calendar class with today's year and date
        cal = Day(self.kwargs['day'],self.kwargs['year'], self.kwargs['month'], date =d)
        

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatday()
        
        context['day'] = mark_safe(html_cal)
        context['prev_day'] = prev_day(d)
        context['next_day'] = next_day(d)
        context['today'] = self.kwargs['day']
        context['month'] = self.kwargs['month']
        context['year'] = self.kwargs['year']
        context['filterwinkelname'] = 'filterwinkel'

        
        
        context['print'] = Service_Apointments.get_print_pdf_url(Service_Apointments, self.kwargs['year'], self.kwargs['month'], self.kwargs['day'] )
        
        
        return context

class FilterDayView(DayView,generic.ListView):
    #login_url = "accounts:signin"

    #print("FilterDayView")
    

    def get_queryset(self):
        
        queryset = Apointments.objects.filter(
             Q(winkel__in=self.request.GET.getlist("winkel")) 
            )   
                            
        return queryset
    
def add_single_event_to_table(table_data,users,i):
    
    table_data.append(['TIJD',users[i].levertijd,'','',i+1,'','','',i+2])
    table_data.append(['PLAATS',users[i].sity,'','','','','',''])
    table_data.append(['POSTC. NR.',users[i].postcode,'','','','','',''])
    table_data.append(['NAAM',users[i].client,'','','','','',''])
    table_data.append(['OPDERNR',users[i].ordernr,'','','','','',''])
    table_data.append(['PRIJS IN €',users[i].price,'','','','','',''])
    table_data.append(['TELEFOON',users[i].telefon,'','','','','',''])
    table_data.append(['WINKEL',users[i].winkel,'','','','','',''])

def add_event_to_table(table_data,users,i):
    
    table_data.append(['TIJD',users[i].levertijd,'','',i+1,users[i+1].levertijd,'','',i+2])
    table_data.append(['PLAATS',users[i].sity,'','','',users[i+1].sity,'',''])
    table_data.append(['POSTC. NR.',users[i].postcode,'','','',users[i+1].postcode,'',''])
    table_data.append(['NAAM',users[i].client,'','','',users[i+1].client,'',''])
    table_data.append(['OPDERNR',users[i].ordernr,'','','',users[i+1].ordernr,'',''])
    table_data.append(['PRIJS IN €',users[i].price,'','','',users[i+1].price,'',''])
    table_data.append(['TELEFOON',users[i].telefon,'','','',users[i+1].telefon,'',''])
    table_data.append(['WINKEL',users[i].winkel,'','','',users[i+1].winkel,'',''])

def add_empty_event_to_table(table_data,i):
    
    table_data.append(['TIJD','','','',i+1,'','','',i+2])
    table_data.append(['PLAATS','','','','','','',''])
    table_data.append(['POSTC. NR.','','','','','','',''])
    table_data.append(['NAAM','','','','','','',''])
    table_data.append(['OPDERNR','','','','','','',''])
    table_data.append(['PRIJS IN €','','','','','','',''])
    table_data.append(['TELEFOON','','','','','','',''])
    table_data.append(['WINKEL','','','','','','',''])

def stylepdf():
    return [('SPAN',(0,0),(0,1)),
                                                          
                                                          
                                                          ('SPAN',(5,0),(8,0)),
                                                          ('ALIGN',(5,0),(8,0),'CENTER'),
                                                          ('SPAN',(5,1),(8,1)),
                                                          ('SPAN',(1,0),(2,0)),
                                                          ('ALIGN',(1,0),(2,1),'CENTER'),
                                                          ('SPAN',(1,1),(2,1)),
                                                          
                                                          ('SPAN',(3,0),(4,0)),
                                                          ('ALIGN',(3,0),(4,1),'CENTER'),
                                                          
                                                          ('SPAN',(3,1),(4,1)),
                                                          ('ALIGN',(0, 42), (-1, -1),'CENTER'),
                                                          ('VALIGN',(0, 42), (-1, -1),'MIDDLE'),
                                                          
                                                          #1
                                                          ('SPAN',(4,2),(4,3)),
                                                          ('ALIGN',(4,2),(4,3),'CENTER'),
                                                          ('VALIGN',(4,2),(4,3),'MIDDLE'),
                                                          
                                                          ('SPAN',(1,2),(3,2)),
                                                          ('SPAN',(1,3),(3,3)),
                                                          
                                                          ('SPAN',(1,4),(4,4)),
                                                          ('SPAN',(1,5),(4,5)),
                                                          ('SPAN',(1,6),(4,6)),
                                                          ('SPAN',(1,7),(4,7)),
                                                          ('SPAN',(1,8),(4,8)),
                                                          
                                                          ('SPAN',(1,9),(4,9)),
                                                          
                                                          ('SPAN',(8,2),(8,3)),
                                                          ('ALIGN',(8,2),(8,3),'CENTER'),
                                                          ('VALIGN',(8,2),(8,3),'MIDDLE'),
                                                          
                                                          ('SPAN',(5,2),(7,2)),
                                                          ('SPAN',(5,3),(7,3)),
                                                          ('SPAN',(5,4),(8,4)),
                                                          ('SPAN',(5,5),(8,5)),
                                                          ('SPAN',(5,6),(8,6)),
                                                          ('SPAN',(5,7),(8,7)),
                                                          ('SPAN',(5,8),(8,8)),
                                                          ('SPAN',(5,9),(8,9)),
                                                          
                                                          #2
                                                          ('SPAN',(4,10),(4,11)),
                                                          ('ALIGN',(4,10),(4,11),'CENTER'),
                                                          ('VALIGN',(4,10),(4,11),'MIDDLE'),
                                                          
                                                          ('SPAN',(1,10),(3,10)),
                                                          ('SPAN',(1,11),(3,11)),
                                                          
                                                          ('SPAN',(1,12),(4,12)),
                                                          ('SPAN',(1,13),(4,13)),
                                                          ('SPAN',(1,14),(4,14)),
                                                          ('SPAN',(1,15),(4,15)),
                                                          ('SPAN',(1,16),(4,16)),
                                                          ('SPAN',(1,17),(4,17)),
                                                          
                                                          ('SPAN',(8,10),(8,11)),
                                                          ('ALIGN',(8,10),(8,11),'CENTER'),
                                                          ('VALIGN',(8,10),(8,11),'MIDDLE'),
                                                          
                                                          ('SPAN',(5,10),(7,10)),
                                                          ('SPAN',(5,11),(7,11)),
                                                          ('SPAN',(5,12),(8,12)),
                                                          ('SPAN',(5,13),(8,13)),
                                                          ('SPAN',(5,14),(8,14)),
                                                          ('SPAN',(5,15),(8,15)),
                                                          ('SPAN',(5,16),(8,16)),
                                                          ('SPAN',(5,17),(8,17)),
                                                          
                                                          #3
                                                          ('SPAN',(4,18),(4,19)),
                                                          ('ALIGN',(4,18),(4,19),'CENTER'),
                                                          ('VALIGN',(4,18),(4,19),'MIDDLE'),
                                                          
                                                          ('SPAN',(1,18),(3,18)),
                                                          ('SPAN',(1,19),(3,19)),
                                                          
                                                          ('SPAN',(1,20),(4,20)),
                                                          ('SPAN',(1,21),(4,21)),
                                                          ('SPAN',(1,22),(4,22)),
                                                          ('SPAN',(1,23),(4,23)),
                                                          ('SPAN',(1,24),(4,24)),
                                                          ('SPAN',(1,25),(4,25)),
                                                          
                                                          ('SPAN',(8,18),(8,19)),
                                                          ('ALIGN',(8,18),(8,19),'CENTER'),
                                                          ('VALIGN',(8,18),(8,19),'MIDDLE'),
                                                          
                                                          ('SPAN',(5,18),(7,18)),
                                                          ('SPAN',(5,19),(7,19)),
                                                          ('SPAN',(5,20),(8,20)),
                                                          ('SPAN',(5,21),(8,21)),
                                                          ('SPAN',(5,22),(8,22)),
                                                          ('SPAN',(5,23),(8,23)),
                                                          ('SPAN',(5,24),(8,24)),
                                                          ('SPAN',(5,25),(8,25)),
                                                           
                                                          #4
                                                          ('SPAN',(4,26),(4,27)),
                                                          ('ALIGN',(4,26),(4,27),'CENTER'),
                                                          ('VALIGN',(4,26),(4,27),'MIDDLE'),
                                                          
                                                          ('SPAN',(1,26),(3,26)),
                                                          ('SPAN',(1,27),(3,27)),
                                                          
                                                          ('SPAN',(1,28),(4,28)),
                                                          ('SPAN',(1,29),(4,29)),
                                                          ('SPAN',(1,30),(4,30)),
                                                          ('SPAN',(1,31),(4,31)),
                                                          ('SPAN',(1,32),(4,32)),
                                                          ('SPAN',(1,33),(4,33)),
                                                          
                                                          ('SPAN',(8,26),(8,27)),
                                                          ('ALIGN',(8,26),(8,27),'CENTER'),
                                                          ('VALIGN',(8,26),(8,27),'MIDDLE'),
                                                          
                                                          ('SPAN',(5,26),(7,26)),
                                                          ('SPAN',(5,27),(7,27)),
                                                          ('SPAN',(5,28),(8,28)),
                                                          ('SPAN',(5,29),(8,29)),
                                                          ('SPAN',(5,30),(8,30)),
                                                          ('SPAN',(5,31),(8,31)),
                                                          ('SPAN',(5,32),(8,32)),
                                                          ('SPAN',(5,33),(8,33)), 
                                                          
                                                          #5
                                                          ('SPAN',(4,34),(4,35)),
                                                          ('ALIGN',(4,34),(4,35),'CENTER'),
                                                          ('VALIGN',(4,34),(4,35),'MIDDLE'),
                                                          
                                                          ('SPAN',(1,34),(3,34)),
                                                          ('SPAN',(1,35),(3,35)),
                                                          ('SPAN',(1,36),(4,36)),
                                                          
                                                          ('SPAN',(1,37),(4,37)),
                                                          ('SPAN',(1,38),(4,38)),
                                                          ('SPAN',(1,39),(4,39)),
                                                          ('SPAN',(1,40),(4,40)),
                                                          ('SPAN',(1,41),(4,41)),
                                                          
                                                          
                                                          ('SPAN',(8,34),(8,35)),
                                                          ('ALIGN',(8,34),(8,35),'CENTER'),
                                                          ('VALIGN',(8,34),(8,35),'MIDDLE'),
                                                          
                                                          ('SPAN',(5,34),(7,34)),
                                                          ('SPAN',(5,35),(7,35)),
                                                          ('SPAN',(5,36),(8,36)),
                                                          ('SPAN',(5,37),(8,37)),
                                                          ('SPAN',(5,38),(8,38)),
                                                          ('SPAN',(5,39),(8,39)),
                                                          ('SPAN',(5,40),(8,40)),
                                                          ('SPAN',(5,41),(8,41)),
                                                          
                                                          #buttom
                                                          ('SPAN',(0,42),(1,42)),
                                                          ('SPAN',(0,43),(1,43)),

                                                          ('SPAN',(2,42),(3,42)),
                                                          ('SPAN',(2,43),(3,43)),
                                                          
                                                          ('SPAN',(4,42),(5,42)),
                                                          ('SPAN',(4,43),(5,43)),
                                                          
                                                          
                                                          ('SPAN',(6,42),(6,43)),
                                                          ('SPAN',(7,42),(8,43)),
                                                          #prise color
                                                                                                              
                                                          ]

def get_pdf_page_by_10_events(doc,users,  buffer,day, month, year):
    
    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
    
    styles.wordWrap = 'CJK' 
    styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', alignment=TA_RIGHT))

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #Q(winkel__in=request.GET.getlist("winkel"))
    

    #elements.append(Paragraph('My User Names', styles['RightAlign']))
  
    table_data = []
    table_data.append(['','DATUM','','DAG','','LOCATIE','','',''])
    table_data.append(['',str(datetime(day, month, year).strftime("%d %B %Y")),'',datetime(day, month, year).strftime('%A'),'','',''])
    #table_data.append(['',str(year) +' '+ str(users[0].start_time.strftime('%B')) +' ' + str(day),'',users[0].start_time.strftime('%A'),'','',''])
  
        
    #print(len(users))   
    list_name = ['TIJD', 'PLAATS','POSTC. NR.', 'NAAM', 'OPDERNR', 'PRIJS IN €', 'TELEFOON', 'WINKEL']
    dict_name = {'TIJD':'start_time', 'PLAATS':'sity','POSTC. NR.':'postcode', 'NAAM':'client', 'OPDERNR':'pk', 'PRIJS IN €':'price', 'TELEFOON':'telefon', 'WINKEL':'winkel'}
    

    count_bloks = 5
    len_event = len(users)
    
    left_event = len_event
    style = stylepdf()
    
    #print(f'len - {len_event}')
    emty_block = (count_bloks*2) - len_event
    
    i = 0
    color_step = 7
    for it in range(len_event):
        if left_event == 0:
            #add_empty_event_to_table(table_data,i)
            continue
            
        
        if left_event - 2 >= 0:
            add_event_to_table(table_data,users,i)
            #if users[i].intern:
            #    style.append(('BACKGROUND',(1,color_step),(4,color_step),colors.red))
            #if users[i+1].intern:
            #    style.append(('BACKGROUND',(5,color_step),(8,color_step),colors.red))
            left_event = left_event - 2
            color_step += 8
            
            
        else:
            add_single_event_to_table(table_data,users,i)
            #if users[i].intern:
            #    style.append(('BACKGROUND',(1,color_step),(4,color_step),colors.red))
            left_event = left_event - 1
       
        
        i = i + 2
        #print(f'count {i}')
        #print(f'left len - {left_event}')
            
    if emty_block%2 != 0:
        emty_block = (emty_block-1)
        
    emty_block = int(emty_block/2)
    #print(emty_block)
    for it in range(emty_block): 
        add_empty_event_to_table(table_data,i)
        i = i + 2  
        
        
        
    table_data.append(['CHAUFFEUR','','BIJRIJDER','', 'KENTEKEN','','NOTTITIE',''])
    table_data.append(['','', '','',''])
    table_data.append(['PIN','CONTACT', 'ONTERN','TOTALE\nINKOMSTEN','TANK\nKOSTEN','BEGINTIJD','EINDTIJD','TOTAL\nUREN','RESTANT'])
    table_data.append(['','', '','','','','','',''])  
    
    '''
    for i, user in enumerate(users):
        # Add a row to the table
        table_data.append([str(user.winkel)
                            +'\n'+ str(user.start_time) 
                            +'\n'+ str(user.sity)
                            +'\n'+ str(user.postcode)
                            +'\n'+ str(user.client)
                            +'\n'+ str(user.start_time)
                            +'\n'+ str(user.start_time)
                            +'\n'+ str(user.telefon)])
    '''
    SPAN_table = [('SPAN',(0,0),(0,1))]
    for i in range(len(list_name)):
        SPAN_table.append(('SPAN',(1,i+4),(4,i+4)))
        SPAN_table.append(('SPAN',(5,i+4),(8,i+4)))
    
   
    # Create the table
    height = [doc.height/50.0]*44
    height.append(30.537795275590554)
    height.append(16.537795275590554)
    
    
    
    #style.append(('BACKGROUND',(1,7),(4,7),colors.red))
    
    user_table = Table(table_data, colWidths=[doc.width/10.0]*10, rowHeights=height, style=style )
    

    user_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                                    
                                    
                                    
                                    
                                    
                                    ('BOX',(4,2),(4,3),2,colors.black),
                                    ('BOX',(8,2),(8,3),2,colors.black),
                                    ('BOX',(4,10),(4,11),2,colors.black),
                                    ('BOX',(8,10),(8,11),2,colors.black),
                                    ('BOX',(4,18),(4,19),2,colors.black),
                                    ('BOX',(8,18),(8,19),2,colors.black),
                                    ('BOX',(4,26),(4,27),2,colors.black),
                                    ('BOX',(8,26),(8,27),2,colors.black),
                                    ('BOX',(4,34),(4,35),2,colors.black),
                                    ('BOX',(8,34),(8,35),2,colors.black),
                                    
                                    
                                    ('BOX',(0,2),(4,9),2,colors.black),
                                    ('BOX',(0,10),(4,17),2,colors.black),
                                    ('BOX',(0,18),(4,25),2,colors.black),
                                    ('BOX',(0,26),(4,33),2,colors.black),
                                    ('BOX',(0,34),(4,41),2,colors.black),
                                    ('BOX',(5,2),(8,9),2,colors.black),
                                    ('BOX',(5,10),(8,17),2,colors.black),
                                    ('BOX',(5,18),(8,25),2,colors.black),
                                    ('BOX',(5,26),(8,33),2,colors.black),
                                    ('BOX',(5,34),(8,41),2,colors.black),
                                    ('INNERGRID', (0, 42), (-1, -1), 2, colors.black),
                                    ('INNERGRID', (0, 0), (8, 1), 2, colors.black),
                                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                                    ('FONTSIZE', (1,2),(8,41), 11),
                                    ('FONTSIZE', (4,2),(4,3), 12),
                                    ('FONTSIZE', (8,2),(8,3), 12),
                                    ('FONTSIZE', (4,10),(4,11), 12),
                                    ('FONTSIZE', (8,10),(8,11), 12),
                                    ('FONTSIZE', (4,18),(4,19), 12),
                                    ('FONTSIZE', (8,18),(8,19), 12),
                                    ('FONTSIZE', (4,26),(4,27), 12),
                                    ('FONTSIZE', (8,26),(8,27), 12),
                                    ('FONTSIZE', (4,34),(4,35), 12),
                                    ('FONTSIZE', (8,34),(8,35), 12),
                                    
                                    ('LEFTPADDING', (0, 42), (-1, -1), 2),             
                                    ('RIGHTPADDING', (0, 42), (-1, -1), 2),             
                                    ('BOTTOMPADDING', (0, 42), (-1, -1), 2),             
                                    ('TOPPADDING', (0, 42), (-1, -1), 2), 
                                    
                                                
                                    ]))
    #elements.append(user_table)
    #elements.append(user_table)
    
    #doc.build(elements)
    return user_table


def generate_pdf(request, day = None, month = None, year = None, date = None):
    if request.user.is_authenticated == False:
        return redirect("http://localhost:8000/")

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    d = datetime.today().strftime('%Y-%m-%d')
    
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    response['Content-Disposition'] = f'inline; filename="{d}.pdf"'

    buffer = BytesIO()
    
    
    
    users = Service_Apointments.objects.filter(start_time__day=year, start_time__month=month, start_time__year=day).order_by("start_time")

    event_by_page = 10
    quant_page = int(math.ceil(len(users)/event_by_page))
    len_users = len(users)
    doc = SimpleDocTemplate(buffer,
                                rightMargin=20,
                                leftMargin=20,
                                topMargin=10,
                                bottomMargin=5, pagesize=A4)
    elements = []
    p_text = "<u>ANEXA 1</u>"
    for  page in range(quant_page):
        
        
        page +=1
        index = (page*10)-10
        
        if len_users < 10:
            #print((page*10)-10,len_users)
            
            user_table = get_pdf_page_by_10_events(doc,users[index:index + len_users], buffer,day, month, year)
        else:
            user_table = get_pdf_page_by_10_events(doc,users[index:page*10], buffer,day, month, year)
            
        len_users -=10
        elements.append(user_table)
        elements.append(Paragraph(str(page), ParagraphStyle(name='RightAlign', fontName='Arial', alignment= TA_CENTER)))
    
    doc.build(elements)
    
    '''
    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer, pagesize =A4)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")
    data = [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]
    
    width = 400
    height = 100
    x = 100
    y = 800
    
    f = Table(data)
    f.wrapOn(p, width, height)
    f.drawOn(p, x, y)
    f.setStyle(TableStyle([('BACKGROUND', (1, 1), (-2, -2), 
          colors.green),
                       ('TEXTCOLOR', (0, 0), (1, -1), colors.red)]))


    # Close the PDF object cleanly.
    p.showPage()
    p.save()
    '''
    
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    
    buffer.close()
    response.write(pdf)
    return response