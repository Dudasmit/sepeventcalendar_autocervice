from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timedelta, date
# Create your models here.




class Service_Apointments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             #default=1,
                             on_delete=models.CASCADE,verbose_name="Gebruiker" )
    

    
    datum = models.DateField(null=True,verbose_name="Datum")
    
    tijd = models.CharField( max_length=47,null=True,verbose_name="Tijd")
    
    
    kenteken = models.CharField( max_length=47,null=True,verbose_name="Kenteken")   
    functie = models.CharField( max_length=150,null=True,verbose_name="functie")   

    price = models.CharField( max_length=47,null=True,verbose_name="Prijs") 
      
    Omschrijving = models.CharField( max_length=500,null=True,verbose_name="Omschrijving")   

    
    
    def __str__(self):
        return f'{self.kenteken}  - {self.datum}'
    
    def save(self, *args, **kwargs):
        
        super(Service_Apointments, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        
        super(Service_Apointments, self).delete(*args, **kwargs)
    
    @property
    def get_html_url(self):
        url = reverse('sepautoservice:event_edit', args=(self.id,))
        delurl = reverse('sepautoservice:delete', args=(self.id,))
        return f'<a href="{url}"> {self.kenteken} - {self.tijd} </a> <!--<a href="{delurl}"> "delete" </a>-->'
    @property
    def get_absolute_url(self):
        return reverse('sepautoservice:event_edit', args=(self.id,))
    
    def get_delete_url(self):
        
        deleteurl = reverse('sepautoservice:delete', args=(self.id,))
        return reverse('sepautoservice:delete', args=(self.id,))
    
    def get_print_pdf_url(self,day, month, year):
        
        url = reverse('sepautoservice:generate_pdf', args=(day, month, year,))
       
        return url
    
    def get_html_url_day(self, day, month, year):
        
        url = reverse('sepautoservice:day', args=(day, month, year,))
        
        return f'<a href="{url}"> {day}</a>'
    
    def get_url_day(self, day, month, year):
        #print(Winkel.get_absolute_url(self))
        
        url = reverse('sepautoservice:day', args=(day, month, year,))

        return url

    