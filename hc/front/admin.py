from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Video
from .models import Faq

# Register your models here.
class FaqAdmin(admin.ModelAdmin):
    """This class displays the Faq details"""
    list_display = ('question', 'answer')

admin.site.register(Faq, FaqAdmin)


class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    """This class displays the Video details"""
    list_display = ('title', 'video')

admin.site.register(Video, VideoAdmin)
