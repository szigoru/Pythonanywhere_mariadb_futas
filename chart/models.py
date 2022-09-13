# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class ChartQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    class Meta:
        db_table = 'chart_question'


class Futasok(models.Model):
    id = models.BigAutoField(primary_key=True)
    distance = models.DecimalField(max_digits=65535, decimal_places=2, blank=True, null=True)
    time = models.CharField(max_length=50, blank=True, null=True)
    idopont = models.CharField(max_length=150, blank=True, null=True)
    komment = models.CharField(max_length=150, blank=True, null=True)  

    class Meta:
        db_table = 'futasok'


       
        
