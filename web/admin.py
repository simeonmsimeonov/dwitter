from django.contrib import admin
from django.contrib.auth.models import Group, User

from web.models import Dweet, Profile
# Register your models here.


class ProfileInLine(admin.StackedInline):
    model = Profile



class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInLine]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Dweet)


