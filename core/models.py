from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.

class Winkel(models.Model):
    name = models.CharField(max_length=47)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        
        super(Winkel, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('winkel', kwargs={"pk": self.pk})
        #return ('winkels', (), {'winkel_id': self.pk}) 

class TypeEvent(models.Model):
    name = models.CharField(max_length=47)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        
        super(TypeEvent, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        print(reverse('typeevents', kwargs={"pk": self.pk}))
        return reverse('typeevents', kwargs={"pk": self.pk})
        #return ('typeevents', (), {'typeevent_id': self.pk}) 



class Apointments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             #default=1,
                             on_delete=models.CASCADE,verbose_name="Gebruiker" )
    
    #typeevent = models.ForeignKey(TypeEvent,on_delete=models.CASCADE,verbose_name="typeevent")

    winkel = models.ForeignKey(Winkel,on_delete=models.CASCADE,verbose_name="Winkel")
    
    start_time = models.DateField(null=True,verbose_name="Datum")
    
    levertijd = models.CharField( max_length=47,null=True,verbose_name="Levertijd van tot")
    
    #end_time = models.DateField(null=True,verbose_name="Datum Tijd")
    
    sity = models.CharField(max_length=47,verbose_name="Plaats")
    postcode = models.CharField(max_length=14) 
    
    #shipping_address = models.CharField(max_length=100,verbose_name="Bezorgadres") 
    ordernr = models.CharField(max_length=47,verbose_name="Order NR") 
    
    #street = models.CharField(max_length=100,verbose_name="Straat") 
    #bildnumb = models.CharField(max_length=100,verbose_name="Huisnummer") 

    price = models.CharField( max_length=47,null=True,verbose_name="Prijs")   
    #intern =   models.BooleanField(default= False)

    
    client = models.CharField(max_length=100,verbose_name="Naam") 
    telefon = models.CharField(max_length=47,verbose_name="Telefoon")
    
    def __str__(self):
        return f'{self.winkel} - {self.sity} - {self.start_time}'
    
    def save(self, *args, **kwargs):
        
        super(Apointments, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        
        super(Apointments, self).delete(*args, **kwargs)
    
    @property
    def get_html_url(self):
        url = reverse('core:event_edit', args=(self.id,))
        delurl = reverse('core:delete', args=(self.id,))
        return f'<a href="{url}"> {self.winkel} - {self.levertijd} </a> <!--<a href="{delurl}"> "delete" </a>-->'
    @property
    def get_absolute_url(self):
        return reverse('core:event_edit', args=(self.id,))
    
    def get_delete_url(self):
        
        deleteurl = reverse('core:delete', args=(self.id,))
        return reverse('core:delete', args=(self.id,))
    
    def get_print_pdf_url(self,day, month, year, winkel):
        
        url = reverse('core:generate_pdf', args=(day, month, year,))
        winkel_filt = ''
        if winkel:
            if len(winkel):
                winkel_filt += '?'
                for win in winkel:
                    winkel_filt += '&winkel='+win
                     
                
            url += winkel_filt
        return url
    
    def get_html_url_day(self, day, month, year, winkel):
        
        url = reverse('core:day', args=(day, month, year,))
        winkel_filt = ''
        if winkel:
            if len(winkel):
                winkel_filt += '/?'
                for win in winkel:
                    winkel_filt += '&winkel='+win
                     
                
            url += winkel_filt

        return f'<a href="{url}"> {day}</a>'
    
    def get_url_day(self, day, month, year):
        #print(Winkel.get_absolute_url(self))
        
        url = reverse('core:day', args=(day, month, year,))

        return url

    