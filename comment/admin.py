from django.contrib import admin

from .models import Comment

from typeidea.custom_site import custom_site

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display=('target','nickname','content','website','created_time')
# Register your models here.
