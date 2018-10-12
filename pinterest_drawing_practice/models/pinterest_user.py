from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User


class PinterestUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='pinterest')

    pinterest_id = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255, blank=True, default='')

    @classmethod
    def create_or_update(cls, pinterest_id, access_token, first_name, last_name):
        created = False
        try:
            pinterest_user = cls.objects.get(pinterest_id=pinterest_id)
        except cls.DoesNotExist:
            created = True
            user = User.objects.create_user(
                username=pinterest_id,
                password=access_token,
                first_name=first_name,
                last_name=last_name,
            )
            pinterest_user = cls.objects.create(
                user=user,
                pinterest_id=pinterest_id,
                access_token=access_token,
            )

        if access_token != pinterest_user.access_token:
            pinterest_user.access_token = access_token
            pinterest_user.user.set_password(access_token)
            pinterest_user.user.save()

        return pinterest_user, created

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


@receiver(post_delete, sender=PinterestUser)
def delete_related_user(sender, **kwargs):
    deleted_profile = kwargs['instance']
    deleted_profile.user.delete()
