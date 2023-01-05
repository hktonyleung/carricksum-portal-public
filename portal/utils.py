from django.utils import timezone
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os



from xhtml2pdf import pisa

def render_to_pdf_obj(template_path, context):
    template = get_template(template_path)
    html  = template.render(context)
    result = BytesIO() 
    pisa_status = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pisa_status.err:
        return result
    return None


#Use on PDF Generation and HTTPResponse
def render_pdf_obj(template_src, result, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    pisa_status = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    return pisa_status

#Use on PDF Generation and HTTPResponse
def render_pdf_file(template_src, context_dict={}):

    result = BytesIO()    
    pisa_status = render_pdf_obj(template_src, result, context_dict)
    if not pisa_status.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def one_weeks_later():
    return (timezone.now() + timezone.timedelta(days=7))

def generate_qrcode(value, size=20):
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(value, image_factory=factory, box_size=size)
    stream = BytesIO()  
    img.save(stream)
    
    return stream.getvalue().decode()


def get_readme():
    """
    Retrieves the README.md. If no such
    entry exists, the function returns None.
    """
    try:

        print(settings.SITE_ROOT)
        f = open(os.path.join(settings.SITE_ROOT, 'README.md'))
        #f = abspath("README.md")
        #print (f)
        #return f.read().decode("utf-8")
        
        return f
    except FileNotFoundError:
        return None
