# -*- coding: utf-8 -*-
import io
import os

from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.core.exceptions import PermissionDenied
from django.db import models, router
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.admin.utils import label_for_field, display_for_field, display_for_value, lookup_field

from django.template.loader import get_template
from django.template import RequestContext
from io import StringIO
import cgi

import csv
# from xhtml2pdf.pisa import pisaDocument
from xhtml2pdf.document import pisaDocument


def export_as_csv_action(description=u"Exportar CSV", fields=None, header=True):
    def export_as_csv(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % modeladmin.opts.db_table

        writer = csv.writer(response)
        if header:
            fields_header = []
            for field_name in fields:
                text, attr = label_for_field(
                    field_name, modeladmin.model,
                    model_admin=modeladmin,
                    return_attr=True
                )
                fields_header.append(text.capitalize())
            writer.writerow(fields_header)

        for obj in queryset:
            line = []
            for field_name in fields:
                f, attr, value = lookup_field(field_name, obj, modeladmin)
                if f is None or f.auto_created:
                    boolean = getattr(attr, 'boolean', False)
                    result_repr = display_for_value(value, boolean)
                else:
                    if isinstance(f, models.ManyToOneRel):
                        field_val = getattr(obj, f.name)
                        if field_val is None:
                            result_repr = '-'
                        else:
                            result_repr = field_val
                    else:
                        result_repr = display_for_field(value, f, '-')
                line.append(strip_tags(u'%s' % result_repr))
            writer.writerow(line)
        return response
    export_as_csv.short_description = description
    return export_as_csv


def report_action(description=u"Impressão", fields=None, header='', template_name='admin/report.html'):
    def report(modeladmin, request, queryset):
        results = {'header': [], 'results': []}
        for field_name in fields:
            text, attr = label_for_field(
                field_name, modeladmin.model,
                model_admin=modeladmin,
                return_attr=True
            )
            results['header'].append(text.capitalize())
            print(text, attr)
        for obj in queryset:
            line = []
            for field_name in fields:
                f, attr, value = lookup_field(field_name, obj, modeladmin)
                if f is None or f.auto_created:
                    boolean = getattr(attr, 'boolean', False)
                    result_repr = display_for_value(value, boolean)
                else:
                    if isinstance(f, models.ManyToOneRel):
                        field_val = getattr(obj, f.name)
                        if field_val is None:
                            result_repr = '-'
                        else:
                            result_repr = field_val
                    else:
                        result_repr = display_for_field(value, f, '-')
                line.append(strip_tags(u'%s' % result_repr))
            results['results'].append(line)

        template = get_template(template_name)
        html = template.render({
            'header': header,
            'results': results,
        })
        result = io.BytesIO()
        pdf = pisaDocument(io.BytesIO(html.encode("UTF-8")), dest=result, link_callback=lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, "")))
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
    report.short_description = description
    return report
