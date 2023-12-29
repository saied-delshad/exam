from django.contrib.auth.models import AbstractUser
from django.db import models


def file_size(value): # add this to some file where you can import it from
    limit = 1.5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1.5 MiB.')

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    # file will be uploaded to MEDIA_ROOT / user_<username>/<filename>
    return 'user_profile/{}.{}'.format(instance.username, ext)


class CustomUser(AbstractUser):

    ATO = models.CharField("Training Organization", max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to = user_directory_path, validators=[file_size], blank=True,
                                        null=True)
    cell_phone = models.CharField('Cell Phone Numeber', max_length=12, blank=True, null=True)
    
    
    @classmethod
    def get_or_create(cls, username=None, *args, **kwargs):
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            user = cls.objects.create_user(username=username, first_name= kwargs.get('first_name'),
                               last_name = kwargs.get('last_name'), email= kwargs.get('email'),
                               cell_phone= kwargs.get('cell_phone'), ATO = kwargs.get('ato'),
                               password=username)
            return user