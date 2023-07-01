import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.html import format_html


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    pdf = pisa.pisaDocument(html, dest=response)
    if not pdf.err:
        return response
    return HttpResponse(format_html('We had some errors<pre>%s</pre>' ))