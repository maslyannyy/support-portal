from django.contrib import admin

from tasks.models import Task, Dictionary, Domain, Feed


@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active', 'script', 'sleep', 'param']
    list_display_links = ['script']
    search_fields = ['script', 'param']

    class Meta:
        model = Task


@admin.register(Dictionary)
class DictionaryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'message']
    list_display_links = ['message']
    search_fields = ['author', 'message']

    class Meta:
        model = Dictionary


@admin.register(Feed)
class FeedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active', 'url', 'is_multi']
    list_display_links = ['url']
    search_fields = ['url']

    class Meta:
        model = Feed


@admin.register(Domain)
class DomainModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active', 'url']
    list_display_links = ['url']
    search_fields = ['url']

    class Meta:
        model = Domain
