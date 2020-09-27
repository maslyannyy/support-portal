from django.contrib import admin

from report_portal.models import Report, Organization, Agent, Organizer, ReportParam


class ReportInstanceInline(admin.StackedInline):
    model = ReportParam
    exclude = ['value', 'slug']
    extra = 0


@admin.register(Report)
class ReportModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'comment']
    list_display_links = ['id', 'title', 'comment']
    search_fields = ['title', 'script', 'comment']
    inlines = [ReportInstanceInline]
    exclude = ['slug']

    class Meta:
        model = Report


@admin.register(Organization)
class OrganizationModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']

    class Meta:
        model = Organization


@admin.register(Agent)
class AgentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'organization']
    list_display_links = ['id', 'name', 'organization']
    search_fields = ['id', 'name']
    list_filter = ['organization']

    class Meta:
        model = Agent


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'organization']
    list_display_links = ['id', 'name', 'organization']
    search_fields = ['id', 'name']
    list_filter = ['organization']

    class Meta:
        model = Organizer
