from django.contrib import admin
from .models import Location, SubwayStation, Classroom, Schedule

admin.site.register(Location)
admin.site.register(SubwayStation)
admin.site.register(Schedule)
admin.site.register(Classroom)
# admin.site.register(Availability)
# admin.site.register(AvailabilityOccurrence)
# admin.site.register(ClassroomReservation)
# admin.site.register(TimeSlot)



