from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, default='')
    area = models.ForeignKey('Area',on_delete=models.CASCADE, null=False, default=1)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(models.Model):
    cpf = models.CharField(primary_key=True,max_length=11,default='')
    id_course = models.ForeignKey('Course',on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30,default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    ra = models.CharField(max_length=7,null=True,blank=True)
    ensino_medio = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=30,default='')

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=30,default='')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50,default='')
    description = models.TextField(default='')
    area = models.ForeignKey('Area',on_delete=models.CASCADE,null=False,default=1)
    organization = models.ManyToManyField('Organization')
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return self.name