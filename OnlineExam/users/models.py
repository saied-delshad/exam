from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    @classmethod
    def get_or_create(cls, username=None, *args, **kwargs):
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            user = cls.objects.create_user(username=username, first_name= kwargs.get('first_name'),
                               last_name = kwargs.get('last_name'), email= kwargs.get('email'),
                               password=username)
            return user