from datetime import datetime
from typing import Union, List, Set, Tuple, Any

from django.db import connections
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from pandas import DataFrame

from helpers import consts
from report_portal import models


def _prepare_table(table: Union[list, set]) -> Union[List[List[Union[str, datetime, int]]],
                                                     Set[Set[Union[str, datetime, int]]]]:
    """Убирайет timezone у datetime, нужно для скачивания в xlsx"""
    for i, line in enumerate(table[:]):
        if type(line) == str:
            continue

        line = list(line)
        for j, cell in enumerate(line[:]):
            if type(cell) == datetime:
                line[j] = datetime.strptime(cell.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            table[i] = tuple(line)
    return table


def get_file(table: Union[List[str], List[Tuple[Any]]], filename: str, format_: str) -> HttpResponse:
    """Помещает table В CSV файл"""
    response = HttpResponse(content_type='Document')
    response['Content-Disposition'] = f'attachment; filename="{filename}.{format_}"'
    df = DataFrame(_prepare_table(table))
    if format_ == consts.CSV:
        df.to_csv(path_or_buf=response, sep=',', index=False, header=False, encoding='UTF-8')
    elif format_ == consts.XLSX:
        df.to_excel(response, index=False, header=False, encoding='UTF-8', sheet_name='Лист 1', engine='xlsxwriter')
    return response


def get_all_reports() -> List[List[str]]:
    """Возвращает все отчеты имеющиеся в БД"""
    all_reports = [[i.title, i.slug, i.comment] for i in models.Report.objects.filter(is_active=True)]
    return sorted(all_reports)


def get_report_if_exist(slug: str) -> Union[models.Report, Http404]:
    """Возвращает отчет или 404"""
    return get_object_or_404(models.Report, slug=slug, is_active=True)


def get_report_params(report_id: int) -> List[List[Union[bool, str, datetime]]]:
    """Возвращает параметры отчеты по id отчета"""
    return list(models.ReportParam.objects.filter(report_id=report_id).values())


def get_report(report_script: str, report_params: list, input_data: dict) -> [List[str], List[Tuple[Any]]]:
    """Снимает отчет с удаленной базы"""
    params_list = []
    sql_str = ''

    for param in report_params:
        if input_data[param['slug']]:
            try:
                value = input_data[param['slug']].strip(' \t\n\r')
            except AttributeError:
                value = input_data[param['slug']]
            sql_condition = param['sql_condition'].strip(' \t\n\r')

            if '{}' in sql_condition:
                params_list.append(sql_condition.format(value))
            else:
                report_script = report_script.replace(sql_condition, value)

    if len(params_list) > 0:
        sql_str = 'WHERE '

    sql_str += ' AND '.join(params_list)
    report_script = report_script.format(sql_str)

    # TODO sql prepare
    with connections['reports'].cursor() as cursor:
        cursor.execute(report_script)
        table_body = cursor.fetchall()
        table_header = [x[0] for x in cursor.description]

    return table_header, table_body
