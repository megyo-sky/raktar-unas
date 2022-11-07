import os
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import pandas as pd

def level():
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'uj_arak.csv')):
        read_file = pd.read_csv(os.path.join(settings.MEDIA_ROOT) + '/uj_arak.csv')
        read_file.to_excel(os.path.join(settings.MEDIA_ROOT) + '/uj_arak.xlsx', index=None, header=True)
        subject, from_email, to = 'Árszinkron', 'szinkron@megaweld.hu', 'megaweldkft@gmail.com'
        text_content = 'Árszinkron'
        html_content = '<p>Árszinkron</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to, "megyoreg@gmail.com"])
        msg.attach_alternative(html_content, "text/html")
        msg.attach_file(os.path.join(settings.MEDIA_ROOT) + '/uj_arak.xlsx')
        msg.send()

    return HttpResponse('Siker', content_type="text/plain")