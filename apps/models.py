from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Model, CharField, BooleanField, ForeignKey, CASCADE, DateTimeField, PositiveIntegerField, \
    OneToOneField


class Group(Model):
    chat_id = CharField(max_length=100, unique=True)
    title = CharField(max_length=255, null=True, blank=True)
    username = CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'groups'
        verbose_name_plural = 'Guruhlar'
        # app_label

    def __str__(self):
        return self.title if self.title else 'Unknown'


class Admin(AbstractUser):
    # telegram_id = CharField(max_length=20)

    class Meta:
        verbose_name = 'Admin '
        verbose_name_plural = 'Adminlar'


class User(Model):
    first_name = CharField(max_length=150, null=True, blank=True)
    last_name = CharField(max_length=150, null=True, blank=True)
    telegram_id = CharField(max_length=20, unique=True)
    date_joined = DateTimeField(auto_now_add=True)
    group_id = CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Userlar'


class InvatedMember(Model):
    # user = ForeignKey('apps.User', CASCADE, 'invited_by')
    # group = ForeignKey('apps.Group', CASCADE, 'invited_groups')
    telegram = CharField(max_length=50)
    chat = CharField(max_length=50)
    invated_users_count = PositiveIntegerField(default=0)
    can_send_message = BooleanField(default=False)

    class Meta:
        db_table = 'invited_members'
        verbose_name = "Odam Qo'shganlar"
        verbose_name_plural = "Odam Qo'shganlar"
        ordering = ['-invated_users_count']


class Settings(Model):
    invite_user_limit = PositiveIntegerField('Eng kam odam qoshish limiti: ', default=20)
    group = OneToOneField('apps.Group', CASCADE)

    class Meta:
        db_table = 'settings'
        verbose_name = 'Sozlama'
        verbose_name_plural = 'Sozlamalar'

    def __str__(self):
        return f'{self.group.title} guruhida eng kam odam qoshish limiti: {self.invite_user_limit} ta'
