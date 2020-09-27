from typing import NamedTuple

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helpers import consts
from helpers.decorators import staff_or_404
from report_portal.forms import PromoForm, ReportForm
from report_portal.services import reports, promocode_generator, catalogs


class FormData(NamedTuple):
    count: int
    length: int
    prefix: str
    postfix: str
    show: str


@login_required
@require_http_methods("GET")
def get_report_by_name(request, slug):

    context = {}

    report = reports.get_report_if_exist(slug)
    report_params = reports.get_report_params(report.id)

    if request.GET:
        form = ReportForm(request.GET, report_params=report_params)
        if form.is_valid():
            form_data = form.cleaned_data

            context['table_headers'], context['table_body'] = reports.get_report(report.script, report_params,
                                                                                 form_data)

            if form_data['show'] in consts.FILE_OPTIONS:
                return reports.get_file(context['table_body'], report.slug, form_data['show'])
    else:
        form = ReportForm(report_params=report_params)

    context['report'] = report
    context['form'] = form

    return render(request, 'report.html', context)


@login_required
@require_http_methods("GET")
def get_all_reports(request):
    all_reports = reports.get_all_reports()
    return render(request, 'reports.html', {'report_list': all_reports})


@login_required
@require_http_methods("GET")
def generate_promo_codes(request):
    context = {}
    if request.GET:
        form = PromoForm(request.GET)

        if form.is_valid():
            form_data = FormData(**form.cleaned_data)
            list_promo = promocode_generator.generate_promo_codes(form_data.count, form_data.length,
                                                                  form_data.prefix, form_data.postfix)

            if form_data.show in consts.FILE_OPTIONS:
                return reports.get_file(list_promo, 'promo_codes', form_data.show)

            context['list_promo'] = list_promo
    else:
        form = PromoForm()

    context['form'] = form
    return render(request, 'generator.html', context)


@staff_or_404
@csrf_exempt
@require_http_methods("POST")
def sync(request, sync_object):
    return JsonResponse({'success': catalogs.sync(sync_object)})


def e_handler404(request, exception):
    return render(request, '404.html', status=404)
