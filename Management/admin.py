from django.contrib import admin
from Management.models import ProjectDetails, ImpactsDirects, ImpactsIndirects, LoadPlan, \
    RefCarbonfootprint, DatacenterReseaux, CompanyDetails, Company


# Register your models here.
admin.site.register(ProjectDetails)
admin.site.register(ImpactsDirects)
admin.site.register(ImpactsIndirects)
admin.site.register(LoadPlan)
admin.site.register(RefCarbonfootprint)
admin.site.register(DatacenterReseaux)
admin.site.register(CompanyDetails)
admin.site.register(Company)