from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, default='')
    duration = models.IntegerField(default=0)

class User(models.Model):
    cpf = models.CharField(primary_key=True,max_length=11,default='')
    id_course = models.ForeignKey('Course',on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30,default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    ra = models.CharField(max_length=7,null=True)