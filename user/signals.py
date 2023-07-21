from .models import Account
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete


def account_creation_update(sender, instance, created, **kwargs):
    if created:
        try:
            user = instance
            Account.objects.create(
                owner=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
        except Exception as e:
            print(e)

    else:
        try:
            user = instance
            account = Account.objects.get(owner=user)
            account.first_name = user.first_name
            account.last_name = user.last_name
            account.email = user.email
            account.save()
        except Exception as e:
            print(e)


def user_deletion(sender, instance, **kwargs):
    try:
        user = User.objects.get(id=instance.owner.id)
        user.delete()
    except Exception as e:
        print(e)


def user_update(sender, instance, created, **kwargs):
    post_save.disconnect(account_creation_update, sender=User)
    if not created:
        try:
            account = instance
            user = User.objects.get(id=account.owner.id)
            user.first_name = account.first_name
            user.last_name = account.last_name
            user.email = account.email
            user.save()
            post_save.connect(account_creation_update, sender=User)
        except Exception as e:
            print(e)


post_save.connect(account_creation_update, sender=User)
post_delete.connect(user_deletion, sender=Account)

post_save.connect(user_update, sender=Account)
