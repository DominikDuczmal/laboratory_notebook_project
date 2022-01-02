from django.contrib import admin
from .models import Analyst, Supervisor, Task

@admin.register(Analyst)
class AnalystAdmin(admin.ModelAdmin):
    """Function registering Admin view of Analyst Model"""

    list_display = ('first_name', 'last_name', 'email', 'laboratory', 'created')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Function registering Admin view of Task Model"""

    readonly_fields = ('date_sent', 'date_completed')


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    """Function registering Admin view of Supervisor Model"""

    list_display = ('laboratory', 'name')
