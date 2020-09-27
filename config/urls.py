from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

handler404 = 'report_portal.views.e_handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('report_portal.urls')),
    path('', include('tasks.urls')),
    path('', include('django.contrib.auth.urls', )),
    path('', RedirectView.as_view(url='/reports/')),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico'), name='favicon'),
]
