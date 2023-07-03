import base64
from django.core.files.base import ContentFile


def photo(photo_data, name):
    format, imgstr = photo_data.split(';base64,')
    img_ext = format.split('/')[-1]
    return ['{}.{}'.format(name, img_ext), ContentFile(base64.b64decode(imgstr))]