from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class ProjectDetails(models.Model):
    projid = models.BigAutoField(db_column='ProjId', primary_key=True)  # Field name made lowercase.
    projectname = models.TextField(db_column='ProjectName')  # Field name made lowercase.
    projectlocation = models.CharField(db_column='ProjectLocation', max_length=50)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True)  # Field name made lowercase.
    whichuserequipment = models.CharField(db_column='WhichUserEquipment', max_length=50, blank=True, null=True)  # Field name made lowercase.
    whichindustrialequipment = models.CharField(db_column='WhichIndustrialEquipment', max_length=50, blank=True, null=True)  # Field name made lowercase.
    buconcerned = models.CharField(db_column='BUConcerned', max_length=50, blank=True, null=True)  # Field name made lowercase.
    projectstatus = models.CharField(db_column='ProjectStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phasetype = models.CharField(db_column='PhaseType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    buildstartdate = models.DateField(db_column='BuildStartDate')  # Field name made lowercase.
    buildenddate = models.DateField(db_column='BuildEndDate')  # Field name made lowercase.
    runstartdate = models.DateField(db_column='RunStartDate')  # Field name made lowercase.
    runenddate = models.DateField(db_column='RunEndDate')  # Field name made lowercase.
    create_timestamp = models.DateTimeField(db_column='Create_Timestamp')  # Field name made lowercase.
    update_timestamp = models.DateTimeField(db_column='Update_Timestamp')  # Field name made lowercase.
    whichindirectparameters = models.CharField(db_column='WhichIndirectParameters', max_length=50, blank=True, null=True)  # Field name made lowercase.
    projectrole = models.CharField(db_column='ProjectRole', max_length=50, blank=True, null=True)  # Field name made lowercase.
    projectdevelopmentphase = models.CharField(db_column='ProjectDevelopmentPhase', max_length=30, blank=True, null=True)  # Field name made lowercase.
    worklocation = models.CharField(db_column='WorkLocation', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PROJECT_DETAILS'

class ImpactsDirects(models.Model):
    directid = models.BigAutoField(db_column='DirectId', primary_key=True)  # Field name made lowercase.
    roleid = models.ForeignKey('LoadPlan', models.DO_NOTHING, db_column='RoleId', blank=True, null=True)  # Field name made lowercase.
    projid = models.ForeignKey('ProjectDetails', models.DO_NOTHING, db_column='ProjId', blank=True, null=True)  # Field name made lowercase.
    projectname = models.TextField(db_column='ProjectName', blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=50, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50)  # Field name made lowercase.
    subcategory = models.CharField(db_column='SubCategory', max_length=50)  # Field name made lowercase.
    phasetype = models.CharField(db_column='PhaseType', max_length=50)  # Field name made lowercase.
    typeoftransport = models.CharField(db_column='TypeOfTransport', max_length=50, blank=True, null=True)  # Field name made lowercase.
    kmtravelledperday = models.BigIntegerField(db_column='KmtravelledPerDay', blank=True, null=True)  # Field name made lowercase.
    vehicleownership = models.CharField(db_column='VehicleOwnership', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totalkmtravelled = models.BigIntegerField(db_column='TotalKmTravelled', blank=True, null=True)  # Field name made lowercase.
    typeofaccomodation = models.CharField(db_column='TypeOfAccomodation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typeoflaptop = models.CharField(db_column='TypeOfLaptop', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mode = models.CharField(db_column='Mode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typeoftelecommuting = models.CharField(db_column='TypeOfTelecommuting', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totalnoofhrsinaday = models.FloatField(db_column='TotalnoofHrsinaday', blank=True, null=True)  # Field name made lowercase.
    totalnoofdays = models.BigIntegerField(db_column='TotalnoofDays', blank=True, null=True)  # Field name made lowercase.
    equipmentownership = models.CharField(db_column='EquipmentOwnership', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typeofequipment = models.CharField(db_column='TypeOfEquipment', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emissionfactor = models.FloatField(db_column='EmissionFactor', blank=True, null=True)  # Field name made lowercase.
    unit = models.TextField(db_column='Unit', blank=True, null=True)  # Field name made lowercase.
    nofworkingdays = models.IntegerField(db_column='NofWorkingDays', blank=True, null=True)  # Field name made lowercase.
    buildstartdate = models.DateField(db_column='BuildStartDate')  # Field name made lowercase.
    buildenddate = models.DateField(db_column='BuildEndDate')  # Field name made lowercase.
    runstartdate = models.DateField(db_column='RunStartdate')  # Field name made lowercase.
    runenddate = models.DateField(db_column='RunEndDate')  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    quarter = models.IntegerField(db_column='Quarter', blank=True, null=True)  # Field name made lowercase.
    totalcarbonfootprint = models.FloatField(db_column='TotalCarbonFootPrint', blank=True, null=True)  # Field name made lowercase.
    workcountry = models.CharField(db_column='WorkCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    create_timestamp = models.DateTimeField(db_column='Create_Timestamp')  # Field name made lowercase.
    update_timestamp = models.DateTimeField(db_column='Update_Timestamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IMPACTS_DIRECTS'


class ImpactsIndirects(models.Model):
    indirectid = models.BigAutoField(db_column='IndirectId', primary_key=True)  # Field name made lowercase.
    roleid = models.ForeignKey('LoadPlan', models.DO_NOTHING, db_column='RoleId', blank=True, null=True)  # Field name made lowercase.
    projid = models.ForeignKey('ProjectDetails', models.DO_NOTHING, db_column='ProjId', blank=True, null=True)  # Field name made lowercase.
    projectname = models.TextField(db_column='ProjectName', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50)  # Field name made lowercase.
    phasetype = models.CharField(db_column='PhaseType', max_length=50)  # Field name made lowercase.
    usecases = models.CharField(db_column='UseCases', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typeoftransport = models.CharField(db_column='TypeOfTransport', max_length=50, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typeofwaste = models.CharField(db_column='TypeOfWaste', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typeofrawmaterial = models.CharField(db_column='TypeOfRawMaterial', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emissionfactor = models.FloatField(db_column='EmissionFactor', blank=True, null=True)  # Field name made lowercase.
    unit = models.TextField(db_column='Unit', blank=True, null=True)  # Field name made lowercase.
    activitydata = models.FloatField(db_column='ActivityData')  # Field name made lowercase.
    runstartdate = models.DateField(db_column='RunStartDate')  # Field name made lowercase.
    runenddate = models.DateField(db_column='RunEndDate')  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    quarter = models.IntegerField(db_column='Quarter', blank=True, null=True)  # Field name made lowercase.
    totalcarbonfootprint = models.FloatField(db_column='TotalCarbonFootPrint', blank=True, null=True)  # Field name made lowercase.
    create_timestamp = models.DateTimeField(db_column='Create_Timestamp')  # Field name made lowercase.
    update_timestamp = models.DateTimeField(db_column='Update_Timestamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IMPACTS_INDIRECTS'


class LoadPlan(models.Model):
    roleid = models.BigAutoField(db_column='RoleId', primary_key=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=50, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    workcountry = models.CharField(db_column='WorkCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    typeofemployee = models.CharField(db_column='TypeOfEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phasetype = models.CharField(db_column='PhaseType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    noofresources = models.IntegerField(db_column='NoOfResources', blank=True, null=True)  # Field name made lowercase.
    noofworkingdays = models.IntegerField(db_column='NoOfWorkingDays', blank=True, null=True)  # Field name made lowercase.
    buildstartdate = models.DateField(db_column='BuildStartDate', blank=True, null=True)  # Field name made lowercase.
    buildenddate = models.DateField(db_column='BuildEndDate', blank=True, null=True)  # Field name made lowercase.
    runstartdate = models.DateField(db_column='RunStartDate', blank=True, null=True)  # Field name made lowercase.
    runenddate = models.DateField(db_column='RunEndDate', blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    quarter = models.IntegerField(db_column='Quarter', blank=True, null=True)  # Field name made lowercase.
    create_timestamp = models.DateTimeField(db_column='Create_Timestamp')  # Field name made lowercase.
    update_timestamp = models.DateTimeField(db_column='Update_Timestamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LOAD_PLAN'


class RefCarbonfootprint(models.Model):
    carbonid = models.BigAutoField(db_column='CarbonId', primary_key=True)  # Field name made lowercase.
    projid = models.ForeignKey(ProjectDetails, models.DO_NOTHING, db_column='ProjId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subcategory = models.CharField(db_column='SubCategory', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lcprod = models.CharField(db_column='LCProd', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lctransport = models.CharField(db_column='LCTransport', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lcusage = models.CharField(db_column='LCUsage', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lcrecycling = models.CharField(db_column='LCRecycling', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lifespanyrs = models.IntegerField(db_column='LifespanYrs', blank=True, null=True)  # Field name made lowercase.
    emissionfactor = models.FloatField(db_column='EmissionFactor', blank=True, null=True)  # Field name made lowercase.
    unit = models.TextField(db_column='Unit', blank=True, null=True)  # Field name made lowercase.
    carbonfootprintperday = models.FloatField(db_column='CarbonFootprintPerDay', blank=True, null=True)  # Field name made lowercase.
    lcunit = models.TextField(db_column='LCUnit', blank=True, null=True)  # Field name made lowercase.
    lcemissionfactor = models.FloatField(db_column='LCEmissionFactor', blank=True, null=True)  # Field name made lowercase.
    yearpublished = models.IntegerField(db_column='YearPublished', blank=True, null=True)  # Field name made lowercase.
    projectusingef = models.TextField(db_column='ProjectUsingEF', blank=True, null=True)  # Field name made lowercase.
    scope = models.CharField(db_column='Scope', max_length=30, blank=True, null=True)  # Field name made lowercase.
    create_timestamp = models.DateTimeField(db_column='Create_Timestamp')  # Field name made lowercase.
    update_timestamp = models.DateTimeField(db_column='Update_Timestamp')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=100, blank=True, null=True)  # Field name made lowercase.
    typeofimpact = models.CharField(db_column='TypeOfImpact', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REF_CARBONFOOTPRINT'


