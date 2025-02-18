from django.db import models

# Create your models here.
class Charles(models.Model):
    password = models.TextField()
    #passwords = models.EmailField(,verbose_name = _('email address'), blank=True)
    class Meta:
        db_table = "charles"
