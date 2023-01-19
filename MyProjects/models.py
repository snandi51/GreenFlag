from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class PROJECT_DETAILS(models.Model):
    ProjId = models.BigIntegerField(primary_key=True)
    ProjectName = models.CharField(max_length=100)
    ProjectLocation_Choices = (("India", "India"), ("Australia", "Australia"),)
    ProjectLocation = models.CharField(max_length=100)
    Department = models.CharField(max_length=100, choices=ProjectLocation_Choices, default='Australia')
    WhichUserEquipment_Choices = (("laptop", "laptop"), ("pc", "pc"), ("tablet", "tablet"),
                                  ("telephone", "telephone"), ("printer", "printer"), ("speakers", "speakers"),
                                  ("projector", "projector"), ("monitor", "monitor"),)
    WhichUserEquipment = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                   choices=WhichUserEquipment_Choices)
    WhichIndustrialEquipment_Choices = (("laptop1", "laptop1"), ("camera", "camera"), ("sensor", "sensor"),
                                        ("lidar", "lidar"),)
    WhichIndustrialEquipment = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                         choices=WhichIndustrialEquipment_Choices)
    WhichParametersImplemented_Choices = (("fuel", "fuel"), ("electricity", "electricity"), ("water", "water"),
                                          ("paper", "paper"), ("plastic", "plastic"), ("waste_material", "waste_material"),
                                          ("raw_material", "raw_material"),)
    WhichParametersImplemented = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                           choices=WhichParametersImplemented_Choices)
    BUConcerned = models.CharField(max_length=100)
    ProjectStatus_Choices = (("approved", "approved"), ("rejected", "rejected"), ("completed", "completed"),)
    ProjectStatus = models.CharField(max_length=100, choices=ProjectStatus_Choices)
    PhaseType = models.CharField(max_length=100)
    BuildStartDate = models.DateField()
    BuildEndDate = models.DateField()
    RunStartDate = models.DateField()
    RunEndDate = models.DateField()
    Year = models.IntegerField()
    Quarter = models.IntegerField()
    Create_Timestamp = models.DateTimeField(auto_now_add=True)
    Update_Timestamp = models.DateTimeField(auto_now_add=True)
