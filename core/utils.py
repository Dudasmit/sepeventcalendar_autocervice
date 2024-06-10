from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Apointments as Event
from django.urls import reverse
from django.db.models import Q

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None,typeevents=None, winkels=None):
		self.year = year
		self.month = month
		self.winkel = winkels
		self.typeevent = typeevents
  
  
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
  
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>' 
   
   
		requests_per_day = events.filter(start_time__day__gte=day,start_time__day__lte=day).order_by('start_time').distinct()
		
		#print(requests_per_day)
		#d = ''
		#for request in requests_per_day:
		#	d += f'<li> {request.get_html_url_day} </li>'

		if day != 0:
			
			return f"<td><span class='date'>{Event.get_html_url_day(Event,day, self.month,self.year,self.winkel)}</span><ul><ol>{d}</ol></ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
     	#Q(winkel__in=self.winkel) ,
		#print(self.typeevent)
		if len(self.winkel):
			events = Event.objects.filter( Q(winkel__in=self.winkel),start_time__year=self.year, start_time__month=self.month)
		else:
			events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
   
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal

def praijs_color(intern):
		if intern:
			return 'red'
		else:
			return ''


class Day(HTMLCalendar):
	def __init__(self, day =None, year=None, month=None, typeevents=None, winkels=None,date = None,):
		self.day = day
		self.year = year
		self.month = month
		self.date = date
		self.winkel = winkels
		self.typeevent = typeevents
		super(Day, self).__init__() 
  
  
 
	def formatday(self):
     
		if self.winkel:
			events_per_day = Event.objects.filter(Q(winkel__in=self.winkel),start_time__day=self.day, start_time__month=self.month, start_time__year=self.year).order_by("start_time")
		else:
			events_per_day = Event.objects.filter(start_time__day=self.day, start_time__month=self.month, start_time__year=self.year).order_by("start_time")

  
  
  
		d = ''
		numb_event = 1
		numb_kolumns = 2
		line_list = ['TIJD','PLAATS','POSTC. NR.','NAAM', 'OPDERNR','PRIJS IN €','TELEFOON','WINKEL']
  
		line_table = ''
		quan_events = len(events_per_day)
		
		quan_page = 3
		left_event = quan_events
		#print(praijs_color(events_per_day[2].intern))
		i = 0
		
		for it in range(quan_events):
			
			if left_event == 0:
				#add_empty_event_to_table(table_data,i)
				continue
            
        
			if left_event - 2 >= 0:
				line_table += f'''<tr style="border: 2px solid;">
    						  <tr><td> TIJD </td> <td> {events_per_day[i].levertijd}</td><td style="text-align: center; vertical-align: middle;" rowspan="2" width="100"><a href="{events_per_day[i].get_absolute_url}"> <div>{i+1}</div></a></td><td> {events_per_day[i+1].levertijd}  </td></td><td style="text-align: center; vertical-align: middle;"  rowspan="2" width="100"><a href="{events_per_day[i+1].get_absolute_url}"> <div>{i+2}</div></a></td></tr>
							  <tr><td> PLAATS </td> <td> {events_per_day[i].sity} </td><td> {events_per_day[i+1].sity} </td></tr>
							  <tr><td> POSTC. NR. </td> <td colspan="2"> {events_per_day[i].postcode} </td><td colspan="2"> {events_per_day[i+1].postcode} </td></tr>
							  <tr><td> NAAM </td> <td colspan="2"> {events_per_day[i].client} </td><td colspan="2"> {events_per_day[i+1].client} </td></tr>
							  <tr><td> OPDERNR </td> <td colspan="2"> {events_per_day[i].ordernr} </td><td colspan="2"> {events_per_day[i+1].ordernr} </td></tr>
							  <tr><td> PRIJS IN € </td> <td colspan="2"  > {events_per_day[i].price} </td><td colspan="2" > {events_per_day[i+1].price} </td></tr>
							  <tr><td> TELEFOON </td> <td colspan="2"> {events_per_day[i].telefon} </td><td colspan="2"> {events_per_day[i+1].telefon} </td></tr>
							  <tr><td width="150"> WINKEL </td> <td colspan="2" width="200"  >{events_per_day[i].winkel}</td><td width="200" colspan="2">{events_per_day[i+1].winkel}</td></tr>
         
   							</tr>'''
				left_event = left_event - 2
            
            
			else:
				line_table += f'''<tr style="border: 2px solid;"><tr><td> TIJD </td> <td> {events_per_day[i].levertijd} </td><td style="text-align: center; vertical-align: middle;" rowspan="2"  width="100"><a href="{events_per_day[i].get_absolute_url}"> <div>{i+1}</div></a></td><td></td><td style="text-align: center; vertical-align: middle;"  rowspan="2" width="100">{i+2}</td></tr>
							  <tr><td> PLAATS </td> <td> {events_per_day[i].sity} </td><td></td></tr>
							  <tr><td> POSTC. NR. </td> <td colspan="2"> {events_per_day[i].postcode} </td><td colspan="2"></td></tr>
							  <tr><td> NAAM </td> <td colspan="2"> {events_per_day[i].client} </td><td colspan="2"></td></tr>
							  <tr><td> OPDERNR </td> <td colspan="2"> {events_per_day[i].ordernr} </td><td colspan="2"></td></tr>
							  <tr><td> PRIJS IN € </td> <td colspan="2"> {events_per_day[i].price} </td><td colspan="2"></td></tr>
							  <tr><td> TELEFOON </td> <td colspan="2"> {events_per_day[i].telefon} </td><td colspan="2"></td></tr>
							  <tr><td width="150"> WINKEL </td> <td colspan="2" width="200">  {events_per_day[i].winkel}</td><td width="200" colspan="2"></td></tr>
         
   							</tr>'''
				left_event = left_event - 1
			i = i + 2
       
        
      
      
      
  
  
  
  
  
		
		for event in events_per_day:
      
			d += f'<tr><td> {event.get_html_url} </td></tr>'
   
		header = '''<table style="border: 2px solid;" border="2" cellpadding="1"  align="center" cellspacing="2" class="">'''
   

		if self.day != 0:
			
			return f"<td><span class='date'>{self.day} {self.date.strftime('%B')} {self.year}</span><ul></ul><ul>{header}<tbody>{line_table}</tbody></table></ul></td>"

		return '<td></td>'
