import io
from xhtml2pdf import pisa
import os
from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.html import format_html
from django.conf import settings


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), dest=result, link_callback=fetch_resource)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse(format_html('We had some errors<pre>%s</pre>' ))

def fetch_resource(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path