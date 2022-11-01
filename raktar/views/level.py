import os
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def level(request):
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'uj_arak.csv')):
        subject, from_email, to = 'Árszinkron', 'szinkron@megaweld.hu', 'megyoreg@gmail.com'
        text_content = 'Árszinkron'
        html_content = '<p>Árszinkron</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.attach_file(os.path.join(settings.MEDIA_ROOT) + '/uj_arak.csv')
        msg.send()

    return HttpResponse('Siker', content_type="text/plain")