from django.urls import path, include

from report_portal.views import (
    get_all_reports,
    generate_promo_codes,
    get_report_by_name,
    sync,
)

reports_url = [
    path('', get_all_reports),
    path('<str:slug>/', get_report_by_name),
]

urlpatterns = [
    path('reports/', include(reports_url)),
    path('generator/', generate_promo_codes),
    path('catalogs/<str:sync_object>/', sync),
]
