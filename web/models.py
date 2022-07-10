from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser,  PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from web.managers import UserManager
from django.utils.text import slugify
from django.core.validators import MinLengthValidator,MaxLengthValidator, MinValueValidator

from web.validators import only_letters_and_numbers_validator, only_letters_validator

DEFAULT_PROFILE_IMG = "http://cdn.onlinewebfonts.com/svg/img_191958.png"



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    username = models.CharField(_('username'), max_length=20, unique=True, validators=(MinLengthValidator(3), MaxLengthValidator(30), only_letters_and_numbers_validator))
    first_name = models.CharField(_('first name'), max_length=30, blank=True, validators=(MinLengthValidator(3), MaxLengthValidator(30), only_letters_validator))
    last_name = models.CharField(_('last name'), max_length=150, blank=True, validators=(MinLengthValidator(3), MaxLengthValidator(30), only_letters_validator))
    bio = models.CharField(max_length=100, blank=True, null=True, validators=(MinLengthValidator(5), MaxLengthValidator(400)))
    profile_image = models.URLField(blank=True, null=True, default=DEFAULT_PROFILE_IMG)
    slug = models.SlugField(max_length=20, unique=True, null=True, blank=True)
    

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)





class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", 
        related_name="followed_by", 
        symmetrical=False, 
        blank=True)
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Dweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="dweets", on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(Tag, related_name="tags", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )
