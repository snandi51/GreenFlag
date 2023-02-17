# importing necessary django classes
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# User class
# class ProjectRolesGroup(AbstractUser):
#     # Define the extra fields
#     # related to User here
#     project_manager = models.CharField(blank=True, max_length=20)
#
#     product_manager = models.CharField(blank=True, max_length=20)
#
#     proxy_po = models.CharField(blank=True, max_length=20)
#
#     data_scientist = models.CharField(max_length=20)
#
#     it_leader1 = models.CharField(blank=True, max_length=20)
#
#     it_leader2 = models.CharField(blank=True, max_length=20)
#
#     it_front = models.CharField(blank=True, max_length=20)
#
#     director_of_data_science = models.CharField(blank=True, max_length=20)
#
#     # More User fields according to need
#
#     # define the custom permissions
#     # related to User.
#     class Meta:
#         permissions = (
#             ("can_go_in_non_ac_bus", "To provide non-AC Bus facility"),
#             ("can_go_in_ac_bus", "To provide AC-Bus facility"),
#             ("can_stay_ac-room", "To provide staying at AC room"),
#             ("can_stay_ac-room", "To provide staying at Non-AC room"),
#             ("can_go_dehradoon", "Trip to Dehradoon"),
#             ("can_go_mussoorie", "Trip to Mussoorie"),
#             ("can_go_haridwaar", "Trip to Haridwaar"),
#             ("can_go_rishikesh", "Trip to Rishikesh"),
#         )
#
#         # Add other custom permissions according to need.
#
